# -*- coding: utf-8 -*-
# !/usr/bin/python
"""
    decorators.py
    ~~~~~~~~~~~~~

        用户权限装饰器
"""

from functools import wraps
from flask import g
from .errors import forbidden


# 超级无敌神奇的修饰器　－　哈哈哈哈哈哈 <- (哈什么哈...) 来自半年后的我
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Permission Error!!!')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
