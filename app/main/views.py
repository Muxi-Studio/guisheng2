# -*- coding: UTF-8 -*-
#!/usr/bin/python
"""
	views.py
	~~~~~~~~~
		桂声app后台视图函数文件
		后台功能实现
"""
import os
import re
import json
import random
import urllib
from datetime import datetime
from flask import render_template, url_for, session, redirect, request, make_response, abort, flash, current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import User, Permission, Role, NewsPost, OriginsPost, IntersPost, NewsComment, OriginsComment, IntersComment
from app import gen_rnd_filename # 随机文件命名


@login_required
@main.route('/index', methods=['GET','POST'])
@main.route('/', methods=['GET','POST'])
def index():
	"""url='/', 实现功能如下:
	   1. 发布文章统计：依据时间排序
	   2. 边栏统计发布文章最多的编辑"""
	news = NewsPost.query.order_by(NewsPost.timestamp.desc()).all()
	return render_template("index.html", news=news)


@login_required
@main.route("/news", methods=['GET','POST'])
def news():
    """url:/news  func: 新闻编辑页面（实现数据的上传）"""
    form = PostForm()
    if form.validate_on_submit():
        post = NewsPost(
			   		body=form.body.data,
			   		author=current_user._get_current_object()
			   )
        db.session.add(post)
        flash("上传成功！")
        return redirect(url_for(".index"))

    return render_template('edit_news.html', form=form)


@login_required
@main.route("/origins", methods=['GET','POST'])
def origins():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = OriginsPost(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for(".index"))

    posts = OriginsPost.query.order_by(OriginsPost.timestamp.desc()).all()
    return render_template("edit.html", form=form, posts=posts)


@login_required
@main.route('/inters', methods=['GET', 'POST'])
def inters():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
	    post = IntersPost(body=form.body.data, author=current_user._get_current_object())
	    db.session.add(post)
	    return redirect(url_for(".index"))

    posts = IntersPost.query.order_by(IntersPost.timestamp.desc()).all()
    return render_template("edit.html", form=form, posts=posts)


@login_required
@main.route("/ckupload/", methods=['OPTIONS','POST'])
def ckupload():
	"""
	集成CKEditor编辑器
	CKEditor是一款富文本编辑器
	CKEditor is a ready-for-use HTML text editor designed to
    simplify web content creation.
    It's a WYSIWYG editor that brings common word processor features directly
    to your web pages.
	Enhance your website experience with our community maintained editor.
	"""
	error = ''
	url = ''
	callback = request.args.get("CKEditorFuncNum")

	if request.method == 'POST' and 'upload' in request.files:
		fileobj = request.files['upload']
		fname, fext = os.path.splitext(fileobj.filename)
		rnd_name = '%s%s' % (gen_rnd_filename(), fext)
		filepath = os.path.join(main.static_folder,'upload',rnd_name)

		# 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except:
				error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
			error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
		    fileobj.save(filepath)
		    url = url_for('.static', filename='%s%s' % ('upload/', rnd_name))
	else:
		error = '提交错误！'

	res = """
	<script type="text/javascript">
	window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
	</script>
	""" % (callback, url, error)
	response = make_response(res)
	response.headers["Content-Type"] = "text/html"
	return response
