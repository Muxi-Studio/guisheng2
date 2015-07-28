# -*- coding:UTF-8 -*-
# !/usr/bin/python
"""
    __init__.py
    ~~~~~~~~~~~
        初始化文件
        １．蓝图注册
        ２．模块导入
"""
from flask import Blueprint

main = Blueprint('main', __name__,static_folder="~/www/project/guisheng/app/static") # static_folder: 静态文件存储目录

from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
