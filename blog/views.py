# -*- coding: utf-8 -*-

from blog import app
from flask import Flask, jsonify, render_template, session, redirect, url_for, request, g, flash, send_from_directory
from blog.mylib import password,comment,Article,artiList
from blog.qiniu import getToken


#异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html'), 404


#
# #自动关闭数据库连接
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db'):
#         g.db.close()



#管理权限认证模块
@app.route('/login', methods = ['GET', 'POST'])
def login():
    pwd = password(request.form.get('passwd'))
    if pwd.check():
        session['log'] = True
        return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('page',pg = 1))



#博客的添加、编辑和删除
@app.route('/new', methods = ['GET', 'POST'])
def new():
    if session.get('log'):
        curArti = Article(0)
        if request.method == 'POST':
            curArti.update(request.form['title'],request.form['tags'],
                           request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('page',pg = 1))
        return render_template('edit.html',curArti = curArti,token=getToken())
    return redirect(url_for('page',pg = 1))
#
# @app.route('/edit/<int:bg_id>', methods = ['GET', 'POST'])
# def edit(bg_id):
#     if session.get('log'):
#         try:
#             curArti = Article(bg_id)
#             curArti.getEdit()
#         except:
#             return redirect(url_for('page',pg = 1))
#         if request.method  == 'POST':
#             curArti.update(request.form['title'],request.form['tags'],request.form['img'],request.form['file'],request.form['editor'])
#             return redirect(url_for('article',bg_id = bg_id))
#         return render_template('edit.html',curArti = curArti,token=getToken())
#     return redirect(url_for('page',pg = 1))
#
# @app.route('/del/<int:id>', methods = ['GET', 'POST'])
# def dele(id):
#     type = request.form.get('type', 2, type=int)
#     pid = request.form.get('pid', -1, type=int)
#     if session.get('log') and pid==id:
#         if type == 0:
#             Article(pid).delArti()
#         elif type ==1:
#             comment(pid).dele()
#     return jsonify(type=type,pid=pid)
#
#
#
# #文章浏览页
# @app.route('/article/<int:bg_id>', methods = ['GET', 'POST'])
# def article(bg_id):
#     if request.method == 'POST' and request.form['comment']:
#         newCom = comment(bg_id)
#         newCom.insert(request.form['comment'],request.form['author'],request.form['reply'])
#         return redirect(url_for('article',bg_id = bg_id))
#     try:
#         curArti = Article(bg_id)
#         curArti.getArti()
#     except:
#         return render_template('error.html'), 404
#     return render_template('article.html',curArti = curArti,id = bg_id)
#
#
#
# #留言板
# @app.route('/memo',methods = ['GET', 'POST'])
# def memo():
#     curCom = comment(0)
#     if request.method == 'POST' and request.form['comment']:
#         curCom.insert(request.form['comment'], request.form['author'], None)
#         return redirect(url_for('memo'))
#     tem = curCom.commList()
#     return render_template('memo.html',tem = tem)
# @app.route('/article/0')
# def arti0():
#     return redirect(url_for('memo'))
#
#
# #许愿池
# @app.route('/wish',methods = ['GET', 'POST'])
# def wish():
#     if request.method == 'POST':
#         flash('许愿池收到了你的愿望,祝你好运！')
#         if request.form['comments']:
#             newWish = comment(-1)
#             newWish.insert(request.form['comments'], request.form['authors'], None)
#             return render_template('wish.html')
#         if request.form['commentm']:
#             newWish = comment(-2)
#             newWish.insert(request.form['commentm'], request.form['authorm'], None)
#             return render_template('wish.html')
#     return render_template('wish.html')



#文章分类、标签检索模块
# @app.route('/')
# def index():
#     curPage = artiList(page=1)
#     curPage.alUpdate()
#     results = curPage.getAl()
#     pmax = curPage.getLen()
#     return render_template('index.html',results = results,pmax = pmax,pg = 1)

# @app.route('/page/<int:pg>')
# def page(pg):
#     curPage = artiList(page=pg)
#     curPage.alUpdate()
#     results = curPage.getAl()
#     pmax = curPage.getLen()
#     if pg > pmax or pg < 1:
#         return render_template('error.html'), 404
#     else:
#         return render_template('page.html',results = results,pmax = pmax,pg = pg)
#
# @app.route('/arch<int:arc>/<int:pg>')
# def arch(arc,pg):
#     curPage = artiList('file',arc,pg)
#     curPage.alUpdate()
#     results = curPage.getAl()
#     pmax = curPage.getLen()
#     if pg > pmax or pg < 1:
#         return render_template('error.html'), 404
#     else:
#         return render_template('page.html',results = results,pmax = pmax,pg = pg)
#
# @app.route('/arch/<tag>/<int:pg>')
# def tag(tag,pg):
#     curPage = artiList('tag',tag,pg)
#     curPage.alUpdate()
#     results = curPage.getAl()
#     pmax = curPage.getLen()
#     if pg > pmax or pg < 1:
#         return render_template('error.html'), 404
#     else:
#         return render_template('page.html',results = results,pmax = pmax,pg = pg)
#
#管理页面
@app.route('/admin')
def admin():
    if session.get('log'):
        tem=comment().getNew()
        return render_template('admin.html',tem = tem)
    else:
        return redirect(url_for('login'))
#
#
# #robots.txt
# @app.route('/robots.txt')
# def static_from_root():
#     return send_from_directory(app.static_folder, request.path[1:])