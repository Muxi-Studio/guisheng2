# coding: utf-8

"""
    authentication.py
    ~~~~~~~~~~~~~~~~~

        API验证文件
        we use flask-httpauth to authenticated my flask web API
"""

from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from . import api
from ..models import User, AnonymousUser
from .errors import unauthorized, forbidden, not_found, server_error


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """验证回调函数(可选：邮件或者令牌)"""
    if email_or_token == '':
        # this is AnonymousUser, don't have email or token
        g.current_user = AnonymousUser()
        return True
    if password == '':
        # do not use password , use token!
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
@auth.login_required
def before_request():
    """run before the each request, and that's
       all the route can get the login_required
       and if you logged in, but you didn't have
       confirmed account, and it will raise 403 error"""
    if g.current_user.is_anonymous:
       return forbidden('Unconfirmed account')


"""error_handler decorater can help us generate json formate error easily"""
@auth.error_handler
def auth_error():
    """验证错误处理(json数据格式)"""
    return unauthorized('Invalid credentials')

@auth.error_handler
def not_found_error():
    return not_found('Not found')

@auth.error_handler
def server_error_error():
    return server_error('Server error')


@auth.login_required
@api.route('/token', methods=["POST", "GET"])
def get_token():
    """token is just a serializer which include user info,
       what you need do is log in the url, and post to the token url
       get the token and use the token login, and that's, it is very
       eazy to tell you(use id), but secret key needed"""
    if g.token_used:
        # that means you can not use token to get token
        return unauthorized('Invalid credentials')
    return jsonify({
        # use the serializer wrap the user id and secret_key
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600  # timelimte json serializer
    })
