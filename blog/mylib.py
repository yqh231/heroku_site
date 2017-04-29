# -*- coding: utf-8 -*-
import datetime

from blogDB import Session
from model import tbl_blog,tbl_comm,tbl_tag

#定义类
class password:
    def __init__(self,pwd):
        self.pwd = pwd
    def check(self):
        import hashlib
        m = hashlib.md5()
        if self.pwd:
            self.pwd +=  '1396'
        else:
            return False
        m.update(self.pwd)
        if m.hexdigest()=='01bf2bf3375b3fbaf8d2dac6dad08c84':
            return True
        else:
            return False

class Article:
    def __init__(self, id):
        self.id = id
        self.session = Session()
    def getExit(self):
        blogdb = get_db()
        cur = blogdb
        cur.execute('SELECT id, title, abstract, tag, date, file FROM blog where id = ?',(self.id,))
        self.exit = cur.fetchall()[0]
        return self.exit
    def getArti(self):
        blogdb = get_db()
        cur = blogdb
        cur.execute('SELECT title, date, content, tag, abstract from blog where id = ?',(self.id,))
        self.arti = cur.fetchall()[0]
        return self.arti
    def getEdit(self):
        blogdb = get_db()
        cur = blogdb
        cur.execute('SELECT title, content,tag from blog where id = ?',(self.id,))
        content = cur.fetchall()[0]
        self.title = content[0]
        self.content = content[1]
        self.tag = content[2]

    def update(self, title, tag, img, file, content):
        abstract = abstr(content,img)
        tags = (tag or '').replace('，',',')
        if self.id:
            blog = self.session.query(tbl_blog).filter(tbl_blog.id == self.id).first()
            blog.title = title
            blog.content = content
            blog.abstract = abstract
            blog.tag = tags
            blog.file = file

            self.session.commit()

        else:
            new_blog = tbl_blog(
                title = title,
                content = content,
                abstract = abstract,
                date = datetime.datetime.now(),
                file = file
            )
            self.session.add(new_blog)
            self.session.commit()

            query_result = self.session.query(tbl_blog.id).order_by(tbl_blog.id.desc()).first()
            self.id = query_result.id

        #delete old tag data
        query_result = self.session.query(tbl_tag).filter(tbl_tag.blog == self.id)
        query_result.delete()

        if tags:
            tags = tags.split(',')
        else:
            tags = []

        for tag in tags:
            new_tag = tbl_tag(
                            tag = tag,
                            blog = self.id
                                )
            self.session.add(new_tag)
        self.session.commit()



    def delArti(self):
        blogdb = get_db()
        cur = blogdb
        cur.execute('DELETE FROM blog WHERE id = ? ',(self.id,))
        cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        cur.execute('DELETE FROM comm WHERE blog = ? ',(self.id,))
        blogdb.commit()

class comment:
    def __init__(self, id = 0 ):
        self.id = id
        self.session = Session()
    def commList(self):
        try:
            blogdb = get_db()
            cur = blogdb
            cur.execute(' SELECT content, date, author, id, reply FROM comm WHERE blog = ? ORDER BY id DESC',(self.id,))
            temp = cur.fetchall() or []
            temp = list(temp)
            temp = map(lambda x:list(x),temp)
            def coSort(x,y):
                xId = x[4] or x[3]
                yId = y[4] or y[3]
                if xId<yId:
                    return 1
                else:
                    return -1
            temp = sorted(temp, coSort)
            def coVeri(x):
                x[4] = x[4] or x[3]
                diff = x[4]-x[3]
                x[4] = diff and u're'
                return x
            self.cList = map(coVeri,temp)
        except:
            self.cList = []
        finally:
            return self.cList
    def getNew(self):
        query_para = (
            tbl_comm.author,
            tbl_comm.id,
            tbl_comm.blog
        )
        query_result = self.session.query(*query_para).order_by(tbl_comm.id.desc())
        temp = query_result.all() or []
        self.cList = temp
        return self.cList

    def insert(self, content, author, reply):
        author = author or u'访客'
        reply = reply or None
        blogdb = get_db()
        cur = blogdb
        cur.execute('insert into comm (content, author, blog, reply) values (?, ?, ?, ?)', (content, author, self.id, reply))
        blogdb.commit()
    def dele(self):
        blogdb = get_db()
        cur = blogdb
        cur.execute('DELETE FROM comm WHERE id = ? ',(self.id,))
        blogdb.commit()

class artiList:
    def __init__(self,method = '',key = '',page = 1):
        self.method = method
        self.key = key
        self.page = ( page - 1 ) * 8
        self.session = Session()
    def getAl(self):
        result = []
        for arti in self.al:
            temp = Article(arti)
            temp = temp.getExit()
            result.append(temp)
        self.result = result
        return self.result
    def getLen(self):
        blogdb = get_db()
        cur = blogdb
        if self.method == 'file':
            cur.execute('SELECT count(*) FROM blog WHERE file = ?;',(self.key,))
        elif self.method == 'tag':
            cur.execute('SELECT count(*) FROM tag WHERE tag = ?;',(self.key,))
        else:
            cur.execute('SELECT count(*) FROM blog;')
        rawlen = cur.fetchall()
        rawlen = int(rawlen[0][0])
        self.len = (rawlen+7)/8 or 1
        return self.len
    def alUpdate(self):
        blogdb = get_db()
        cur = blogdb
        if self.method == 'file':
            cur.execute(' SELECT id FROM blog WHERE file = ? ORDER BY id DESC LIMIT 8 OFFSET ?',(self.key,self.page,))
        elif self.method == 'tag':
            cur.execute('select blog from tag where tag = ? LIMIT 8 OFFSET ?',(self.key,self.page,))
        else:
            cur.execute(' SELECT id FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(self.page,))
        altemp = cur.fetchall()
        altemp = map(lambda x: int(x[0]),altemp)
        altemp.sort(reverse = True)
        self.al = altemp
        return self.al

def abstr(text,img = ""):
    text = text[:1200]
    text = text.replace(u'&nbsp;',u' ')
    text = text.replace(u'</p',u'\n<')
    text = text.replace(u'</b',u'\n<')
    text = text.replace(u'</h',u'\n<')
    text = text.replace(u'<br>',u'\n')
    def fn(x, y):
        if x[-1] == "<" and y != ">":
            return x
        else:
            return x+y
    text = reduce(fn,text)
    text = text.replace(u'<>',u'')
    text = text.replace(u'\n\n\n',u'\n')
    text = text.replace(u'\n\n',u'\n')
    text = text[:120]+'...'+img
    return text

def exper1():
    cur=get_db()
    cur.execute('''SELECT TAG, COUNT(*) FROM TAG GROUP BY TAG ORDER BY ID DESC;''')
    print cur.fetchall()


