# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    decorators.py
    ~~~~~~~~~~~~~
    api修饰器文件
"""
from functools import wraps
from flask import g
from .errors import forbidden

# 超级无敌神奇的修饰器　－　哈哈哈哈哈哈
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('权限错误!')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
