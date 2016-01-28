# coding: utf-8
from . import main
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user, logout_user, login_user
from .forms import LoginForm, EditForm
from app.models import User, NewsPost, OriginsPost, IntersPost
from app import db


"""登录"""
@main.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # 采用邮箱登录
        if user is not None and \
            user.verify_password(form.password.data) \
                and user.is_administrator():
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        else:
            flash("用户名或密码不存在")
    return render_template('main/index.html', form=form)


"""登出"""
@main.route('/logout/')
@login_required
def logout():
    """登出"""
    logout_user()
    flash('你已登出!')
    return redirect(url_for('main.login'))


"""首页[R, D, U]"""
@main.route('/')
@main.route('/dashboard/')
@login_required
def dashboard():
    """
    展示:
        1. 新闻文章 news
        2. 原创图集 pics
        3. 互动话题 topics
    """
    news = NewsPost.query.all()
    pics = OriginsPost.query.all()
    topics = IntersPost.query.all()
    return render_template('main/dashboard.html',
        news=news, pics=pics, topics=topics)


"""新闻发布页[C]"""
@main.route('/news/', methods=['GET', 'POST'])
@login_required
def news():
    """
    对新闻板块的操作
    1. 发布新闻(ckeditor编辑器)
    2. 删除新闻
    """
    form = EditForm()
    if form.validate_on_submit():
        news = NewsPost(
            title = form.title.data,
            body_html = form.post.data,
            author_id = current_user.id,
        )
        db.session.add(news)
        db.session.commit()
        flash('新闻发布成功!')
        return redirect(url_for('main.news'))
    return render_template('main/forms.html', form=form)


"""特定的新闻阅读[R]"""
@main.route('/read_news/<int:id>/')
# @login_required
def read(id):
    news = NewsPost.query.get_or_404(id)
    return render_template('main/news.html', news=news)


"""开启ckeditor上传接口"""
@main.route('/ckupload/')
def ckupload():
    form = EditForm()
    response = form.upload(endpoint=main)
    return response

