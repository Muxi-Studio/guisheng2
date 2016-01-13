# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    comments.py
    ~~~~~~~~~~~

        1. 获取相关板块的评论
        2. 用户撰写评论
"""

from . import api
from .. import db
from .authentication import auth
from flask import jsonify, request, g, url_for, current_app
from ..models import NewsPost, OriginsPost, IntersPost, Permission, NewsComment, IntersComment, OriginsComment
from .decorators import permission_required # <-- 那个邻家的超级无敌可爱装饰器`` # <-- (突然发现我那时候好😓 )


# @api.route('/newscomments/')
# def get_newscomments():
#     page = request.args.get('page', 1, type=int)
#     pagination = NewsComment.query.order_by(NewsComment.timestamp.desc()).paginate(
#         page,
#         per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False
#     )
#     newscomments = pagination.items
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_newscomments', page=page-1, _external=True)
#     next = None
#     if pagination.has_next:
#         next = url_for('api.get_newscomments', page=page+1, _external=True)
#     return jsonify({
#         'posts': [comment.to_json() for comment in newscomments],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })
# 
# 
# @api.route('/originscomments')
# def get_originscomments():
#     page = request.args.get('page', 1, type=int)
#     pagination = OriginsComment.query.order_by(OriginsComment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False
#     )
#     originscomments = pagination.items
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_originscomments', page=page-1, _external=True)
#     next = None
#     if pagination.has_next:
#         next = url_for('api.get_originscomments', page=page+1, _external=True)
#     return jsonify({
#         'posts': [comment.to_json() for comment in originscomments],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })
# 
# 
# @api.route('/interscomments')
# def get_interscomments():
#     page = request.args.get('page', 1, type=int)
#     pagination = IntersComment.query.order_by(IntersComment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False
#     )
#     interscomments = pagination.items
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_interscomments', page=page-1, _external=True)
#     next = None
#     if pagination.has_next:
#         next = url_for('api.get_interscomments', page=page+1, _external=True)
#     return jsonify({
#         'posts': [comment.to_json() for comment in interscomments],
#         'prev': prev,
#         'next': next,
#         'count': pagination.total
#     })
# 
# 
# @api.route('/newscomments/<int:id>')
# def get_newscomment(id):
#     comment = NewsComment.query.get_or_404(id)
#     return jsonify(comment.to_json())
# 
# 
# @api.route('/originscomments/<int:id>')
# def get_originscomment(id):
#     comment = OriginsComment.query.get_or_404(id)
#     return jsonify(comment.to_json())
#
#
# @api.route('/interscomments/<int:id>')
# def get_interscomment(id):
#     comment = IntersComment.query.get_or_404(id)
#     return jsonify(comment.to_json())


@api.route('/news/<int:id>/comments/')
def get_news_id_comments(id):
    """ 获取特定id的评论 """
    news = NewsPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = news.comments.order_by(NewsComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['GUISHENGAPP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_news_id_comments', id = id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_news_id_comments', id = id, page=page+1, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/origins/<int:id>/comments/')
def get_origins_id_comments(id):
    origins = OriginsPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(OriginsComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['GUISHENGAPP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_origins_id_comments', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_origins_id_comments', id=id, page=page+1, _external=True)
    return jsonify({
        'comment': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/inters/<int:id>/comments')
def get_inters_id_comments(id):
    comment = IntersPost.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(IntersComment.timestamp.asc()).paginate(
        page, per_page=current_app.config['GUISHENGAPP_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_inters_id_comments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_inters_id_comments', page=page+1, _external=True)
    return jsonify({
        'comment': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/news/<int:id>/comments/', methods=['POST', 'GET'])
@auth.login_required
@permission_required(Permission.COMMENT)
def new_news_comment(id):
    """ 接受request body, 更新评论信息 """
    comment = NewsComment.from_json(request.json)
    comment.author_id = g.current_user.id
    comment.news_id = id
    db.session.add(comment)
    db.session.commit()
    return jsonify(
        comment.to_json()
    ), 201


@api.route('/origins/<int:id>/comments/', methods=['POST', 'GET'])
@auth.login_required
@permission_required(Permission.COMMENT)
def new_origins_comment(id):
    comment = OriginsComment.from_json(request.json)
    comment.author_id = g.current_user.id
    comment.news_id = id
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201


@api.route('/inters/<int:id>/comments/', methods=['POST', 'GET'])
@auth.login_required
@permission_required(Permission.COMMENT)
def new_inters_comment(id):
    post = IntersPost.query.get_or_404(id)
    comment = IntersComment.from_json(request.json)
    comment.author_id = g.current_user.id
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201
