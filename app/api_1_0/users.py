# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    users.py
    ~~~~~~~~
        用户API文件
        1. 获取用户信息
        2. 获取用户发布的文章
        3. 获取用户发布的评论
        4. 修改用户信息
"""
from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, NewsPost, OriginsPost, IntersPost


@api.route('/users/<int:id>')
def get_user(id):
    """获取特定id用户的信息"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


# ----- 特定对作者 ------
@api.route('/users/<int:id>/news/')
def get_user_news(id):
    """获取特定作者发布的新闻文章集合"""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.news.order_by(NewsPost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    news = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_news', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_news', page=page+1, _external=True)
    return jsonify({
        'news': [post.to_json() for post in news],
		'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/origins/')
def get_user_origins(id):
    """获取特定作者发布的原创文章集合"""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.origins.order_by(OriginsPost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    origins = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_origins', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_origins', page=page+1, _external=True)
    return jsonify({
        'origins': [post.to_json() for post in origins],
        'prev': prev,
        'next': next,
        'count': pagination.total
	})


@api.route('/users/<int:id>/inters/')
def get_user_inters(id):
    """获取特定作者发布的互动文章"""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.inters.order_by(IntersPost.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    inters = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_inters', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_inters', page=page+1, _external=True)
    return jsonify({
        'inters': [post.to_json() for post in inters],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
