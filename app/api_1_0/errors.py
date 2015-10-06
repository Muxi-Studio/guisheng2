# coding: utf-8

"""
    errors.py
    ~~~~~~~~~

        api 错误处理文件
        利用内容协商机制，将html错误响应转变为json格式响应
"""

from flask import jsonify
from app.exceptions import ValidationError
from . import api


def not_found(message):
    """404无法找到"""
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


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


def server_error(message):
    """服务器内部错误"""
    response = jsonify({'error': 'server error', 'message':message})
    response.status_code = 500
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
