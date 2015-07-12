# -*- coding: utf-8 -*-
# !usr/bin/python
"""
    errors.py
    ~~~~~~~~~
    api 错误处理文件
"""
from flask import jsonify
from app.exceptions import ValidationError
from . import api

def bad_request(message):
    """错误请求处理"""
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

def unauthorized(message):
    """验证错误处理"""
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

def forbidden(message):
    """禁止访问"""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
