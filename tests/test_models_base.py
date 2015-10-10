# coding: utf-8

"""
    test_models_base.py
    ~~~~~~~~~~~~~~~~~~~

        数据库模型测试基类

        class TestBaseModel
            setUp(): 创建环境

            tearDown(): 销毁环境
"""

import unittest
from app import create_app, db
from app.models import Role


class TestBaseModel(unittest.TestCase):
    """
    数据库测试基类，
    创建测试环境
    销毁测试环境
    """
    def setUp(self):
        # 创建flask object实例
        self.app = create_app('testing')
        # 创建程序上下文
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建测试数据库(生成用户角色)
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
