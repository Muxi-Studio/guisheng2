# coding: UTF-8

"""
	views.py
	~~~~~~~~~
		桂声app后台视图函数文件
		后台功能实现
"""

from flask import render_template, url_for, redirect, request, flash, current_app
from flask.ext.login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import NewsPost, OriginsPost, IntersPost


@login_required
@main.route('/index', methods=['GET','POST'])
@main.route('/', methods=['GET','POST'])
def index():
	"""url='/', 实现功能如下:
	   1. 发布文章统计：依据时间排序
	   2. 边栏统计发布文章最多的编辑
	   3. 添加分页功能"""
	page = request.args.get('page', 1, type=int)
	pagination = NewsPost.query.order_by(NewsPost.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False
	)
	news = pagination.items
	return render_template("index.html", news=news, pagination=pagination)


@login_required
@main.route("/news", methods=['GET','POST'])
def news():
    """url:/news  func: 新闻编辑页面（实现数据的上传）"""
    form = PostForm()
    if form.validate_on_submit():
        post = NewsPost(
					title=form.title.data,
			   		body=form.body.data,
			   		author=current_user._get_current_object()
		)
        db.session.add(post)
        flash("上传成功！")
        return redirect(url_for(".index"))

    return render_template('edit.html', form=form)


@login_required
@main.route("/origins", methods=['GET','POST'])
def origins():
    """url:/origins  func: 原创编辑页面（实现数据的上传）"""
    form = PostForm()
    if form.validate_on_submit():
        post = OriginsPost(
					title=form.title.data,
			   		body=form.body.data,
			   		author=current_user._get_current_object()
		)
        db.session.add(post)
        flash("上传成功！")
        return redirect(url_for(".index"))

    return render_template('edit.html', form=form)


@login_required
@main.route("/inters", methods=['GET','POST'])
def inters():
    """url:/inters  func: 新闻编辑页面（实现数据的上传）"""
    form = PostForm()
    if form.validate_on_submit():
        post = IntersPost(
					title=form.title.data,
			   		body=form.body.data,
			   		author=current_user._get_current_object()
		)
        db.session.add(post)
        flash("上传成功！")
        return redirect(url_for(".index"))

    return render_template('edit.html', form=form)


@main.route('/ckupload/', methods=["POST", "GET"])
def ckupload():
    form = PostForm()
    response = form.upload(endpoint=main)
    return response
