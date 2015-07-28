# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    post.py
    ~~~~~~~
        用户文章(图集)API --- 对文章资源的处理
        1. 获取文章信息(id 单个文章信息)
        /news/; /origins/; /inters/
        2. 获取文章的作者（用户中的一员--特定权限的人）
        /news/user/; /origins/user; /inters/user
        3. 获取文章图集的评论(id 特定的评论)
        /news/comment; /origins/comment; /inters/comment
        4. put单个文章
        5. post文章集合
"""
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import NewsPost, OriginsPost, IntersPost, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/news/')
def get_news():
    """获取新闻板块的文章(包括图片)"""
    page = request.args.get('page', 1, type = int)
    pagination = NewsPost.query.paginate(
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


@api.route('/origins/')
def get_origins():
    """获取原创板块的图集和文章"""
    page = request.args.get('page', 1, type=int)
    pagination = OriginsPost.query.paginate(
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


@api.route('/inters/')
def get_inters():
    page = request.args.get('page', 1, type=int)
    pagination = IntersPost.query.paginate(
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


@api.route('/news/<int:id>')
def get_news_id(id):
    """获取特定id的新闻文章"""
    post = NewsPost.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/origins/<int:id>')
def get_origins_id(id):
    """获取特定id的原创文章"""
    post = OriginsPost.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/inters/<int:id>')
def get_inters_id(id):
    """获取特定id的互动文章"""
    post = IntersPost.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/news/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_news():
    """post新闻文章集合"""
    post = NewsPost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/origins/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_origins():
    """post原创文章集合"""
    post = OriginsPost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/inters/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_inters():
    """post互动文章集合"""
    post = IntersPost.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/news/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_news(id):
    """puts 特定id的新闻文章"""
    post = NewsPost.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('你不具备修改权限!')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/origins/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_origins(id):
    """puts 特定id的原创文章"""
    post = OriginsPost.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('你不具备修改权限!')
    post.body = request.json.get('body', post.body)
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/inters/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_inters(id):
    """puts 特定id的互动文章"""
    post = IntersPost.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('你不具备修改权限!')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
