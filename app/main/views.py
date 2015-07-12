# -*- coding: UTF-8 -*- 
#!/usr/bin/python
import os
import re
import json
import random
import urllib

from datetime import datetime
from flask import render_template,url_for,session,redirect,request,make_response,abort,flash,current_app
from flask.ext.login import login_required,current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import User,Permission, Role, NewsPost,OriginsPost,IntersPost,NewsComment, OriginsComment, IntersComment
from app import gen_rnd_filename

@main.route('/',methods=['GET','POST'])
def index():
	return render_template("index.html")

@main.route("/news",methods=['GET','POST'])
def news():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = NewsPost(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for(".index"))

    posts = NewsPost.query.order_by(NewsPost.timestamp.desc()).all()
    return render_template('edit.html',form=form,posts=posts)

@main.route("/origins",methods=['GET','POST'])
def origin():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = OriginPost(body=form.body.data,author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for(".index"))

    posts = OriginPost.query.order_by(OriginPost.timestamp.desc()).all()
    return render_template("edit.html",form=form,posts=posts)
"""
@main.route("/zonghe",methods=['GET','POST'])
#    form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
	    post = ZonghePost(body=form.body.data,author=current_user._get_current_object())
	    db.session.add(post)
	    return redirect(url_for(".index"))
    posts = ZonghePost.query.order_by(Post.timestamp.desc()).all()
    return render_template("edit.html",form=form,posts=posts)
"""
@main.route("/ckupload/",methods=['OPTIONS','POST'])
def ckupload():
	"""CKEditor file upload"""
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
