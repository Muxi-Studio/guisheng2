# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    comments.py
    ~~~~~~~~~~~

        获取评论信息的API
        １．评论的作者
        修改评论
"""

from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import NewsPost, OriginsPost, IntersPost, Permission, NewsComment, IntersComment, OriginsComment
from . import api
from .decorators import permission_required # <-- 那个邻家的超级无敌可爱修饰器``


@api.route('/newscomments')
def get_newscomments():
    page = request.args.get('page', 1, type=int)
    pagination = NewsComment.query.order_by(NewsComment.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    newscomments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_newscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_newscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in newscomments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/originscomments/')
def get_originscomments():
    page = request.args.get('page', 1, type=int)
    pagination = OriginsComment.query.order_by(OriginsComment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    originscomments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_originscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_originscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in originscomments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/interscomments/')
def get_interscomments():
    page = request.args.get('page', 1, type=int)
    pagination = IntersComment.query.order_by(IntersComment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    interscomments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_interscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_interscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in interscomments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/newscomments/<int:id>')
def get_newscomment(id):
    comment = NewsComment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/originscomments/<int:id>')
def get_originscomment(id):
    comment = OriginsComment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/interscomments/<int:id>')
def get_interscomment(id):
    comment = IntersComment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/news/<int:id>/comments/')
def get_news_comments(id):
    post = NewsPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(NewsComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_newscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_newscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/origins/<int:id>/comments/')
def get_origins_comments(id):
    post = OriginsPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(OriginsComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_originscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_originscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/inters/<int:id>/comments/')
def get_inters_comments(id):
    post = IntersPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(IntersComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_interscomments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_interscomments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/news/<int:id>/comments/', methods=['POST', 'GET'])
@permission_required(Permission.COMMENT)
def new_news_comment(id):
    comment = NewsComment.from_json(request.json)
    comment.author = g.current_user
    comment.news_id = id
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, {'Location': url_for('api.get_newscomment', id=comment.id, _external=True)}


@api.route('/origins/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_origins_comment(id):
    comment = OriginsComment.from_json(request.json)
    comment.author = g.current_user
    comment.news_id = id
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, {'Location': url_for('api.get_originscomment', id=comment.id, _external=True)}


@api.route('/inters/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_inters_comment(id):
    post = IntersPost.query.get_or_404(id)
    comment = IntersComment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, {'Location': url_for('api.get_interscomment', id=comment.id, _external=True)}
