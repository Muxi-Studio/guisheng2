# coding: utf-8

"""
    __init__.py
    ~~~~~~~~~~~

        api初始化文件
        １．创建蓝图
        ２. 导入模块(从当前文件夹中导入)

"""

from flask import Blueprint


api = Blueprint('api', __name__) # 注册了一个API蓝图


from . import authentication, posts ,users, comments, errors
