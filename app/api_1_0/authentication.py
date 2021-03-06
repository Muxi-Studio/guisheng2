# coding: utf-8

"""
    authentication.py
    ~~~~~~~~~~~~~~~~~

    API验证文件

"""

from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import current_user
from . import api
from ..models import User, AnonymousUser
from .errors import unauthorized, forbidden, not_found, server_error


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """ token 验证"""
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        # 使用token无须提供用户名和密码
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    # 否则使用email查询到用户
    # 然后验证密码
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
def before_request():
    pass


"""
error_handler decorater can help us generate json formate error easily
"""
# 403
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

# 404
@auth.error_handler
def not_found_error():
    return not_found('Not found')

# 500
@auth.error_handler
def server_error_error():
    return server_error('Server error')


@api.route('/token/', methods=["POST", "GET"])
@auth.login_required
def get_token():
    """ get token """
    if isinstance(g.current_user, AnonymousUser) or g.token_used:
        return unauthorized('Invalid credentials')  # => in json format
    return jsonify({
        'token': g.current_user.generate_auth_token(3600),
        'expiration': 3600,
        'id' : g.current_user.id
    })
