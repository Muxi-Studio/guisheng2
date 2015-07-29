# -*- coding: UTF-8 -*-
#!/usr/bin/python
"""
    __init__.py
    ~~~~~~~~~~~~

    1. auth 包模块导入文件
    2. 用户认证蓝图创建
"""
from flask import Blueprint


auth = Blueprint('auth',__name__)


from . import views
