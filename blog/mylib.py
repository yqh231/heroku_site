# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import func
from markdown2 import markdown

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
        query_result = self.session.query(tbl_blog).filter(tbl_blog.id == self.id).first()
        self.exit = query_result
        return self.exit
    def getArti(self):
        query_result = self.session.query(tbl_blog).filter(tbl_blog.id == self.id).first()
        self.arti = query_result
        return self.arti
    def getEdit(self):
        query_result = self.session.query(tbl_blog).filter(tbl_blog.id == self.id).first()
        self.title = query_result.title
        self.content = query_result.content
        self.tag = query_result.tag

    def update(self, title, tag, img, file, content):
        abstract = abstr(content,img)
        content = abstr_content(content)
        tags = (tag or '').replace('，',',')
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'blockquote', 'em', 'i',
                        'strong', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        extensions = ["codehilite",'fenced-code-blocks']
        if self.id:
            blog = self.session.query(tbl_blog).filter(tbl_blog.id == self.id).first()
            blog.title = title
            blog.content = markdown(content, ["nl2br", "codehilite","footnotes"])
            blog.abstract = markdown(abstract, ["nl2br", "codehilite","footnotes"])
            blog.tag = tags
            blog.file = file

            self.session.commit()

        else:
            new_blog = tbl_blog(
                title = title,
                content = markdown(content, extras = extensions),
                abstract = markdown(abstract, extras = extensions),
                tag = tags,
                date = datetime.datetime.now(),
                file = file,
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
        query_result = self.session.query(tbl_blog).filter(tbl_blog.id == self.id)
        query_result.delete()
        query_result = self.session.query(tbl_tag).filter(tbl_tag.blog == self.id)
        query_result.delete()
        query_result = self.session.query(tbl_comm).filter(tbl_comm.blog == self.id)
        query_result.delete()

        self.session.commit()

class comment:
    def __init__(self, id = 0 ):
        self.id = id
        self.session = Session()
    def commList(self):
        try:
            query_result = self.session.query(tbl_comm).filter(tbl_comm.blog == self.id).order_by(tbl_comm.blog.desc()).all()
            temp = query_result or []
            print temp
            self.cList = temp
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

    def insert(self, content, author, reply = None):
        author = author or u'访客'
        reply = reply or None
        new_comm = tbl_comm(
            author = author,
            blog = self.id,
            content = content,
            reply = reply,
            date = datetime.datetime.now()
        )
        self.session.add(new_comm)
        self.session.commit()
    def dele(self):
        query_results = self.session.query(tbl_comm).filter(tbl_comm.id == self.id)
        query_results.delete()
        self.session.commit()

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
        if self.method == 'file':
            query_result = self.session.query(func.count(tbl_blog.id).label('count'))\
                .filter(tbl_blog.file == self.key)
        elif self.method == 'tag':
            query_result = self.session.query(func.count(tbl_tag.id).label('count'))\
                .filter(tbl_tag.tag.like(self.key))
        else:
            query_result = self.session.query(func.count(tbl_blog.id).label('count'))
        rawlen = query_result.first()
        rawlen = int(rawlen.count)
        self.len = (rawlen+7)/8 or 1
        return self.len
    def alUpdate(self):
        if self.method == 'file':
            query_result = self.session.query(tbl_blog.id).filter(tbl_blog.file == self.key)\
                                .order_by(tbl_blog.id.desc()).limit(8).all()
        elif self.method == 'tag':
            query_result = self.session.query(tbl_tag.blog)\
                .filter(tbl_tag.tag.like(self.key)).limit(8).offset(self.page).all()
        else:
            query_result = self.session.query(tbl_blog.id).order_by(tbl_blog.id.desc()).\
                limit(8).offset(self.page).all()
        altemp = query_result
        altemp = map(lambda x: int(x[0]),altemp)
        altemp.sort(reverse = True)
        self.al = altemp
        return self.al

def abstr_content(text):
    text = text.replace(u'&nbsp;', u' ')
    text = text.replace(u'</p', u'\n<')
    text = text.replace(u'</b', u'\n<')
    text = text.replace(u'</h', u'\n<')
    text = text.replace(u'<br>', u'\n')

    def fn(x, y):
        if x[-1] == "<" and y != ">":
            return x
        else:
            return x + y

    text = reduce(fn, text)
    text = text.replace(u'<>', u'')
    text = text.replace(u'\n\n\n', u'\n')
    text = text.replace(u'\n\n', u'\n')
    return text


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


