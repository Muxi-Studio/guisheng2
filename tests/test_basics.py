# coding: UTF-8
# !/usr/bin/env python
"""
    test_basics.py
    ~~~~~~~~~~~~~~

    测试：
        app
"""
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """
        创建一个测试环境
        　　１.利用工厂函数创建一个测试实例
            2.激活程序上下文（确保可以使用 current_app）
            3.创建一个测试数据库
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        1.删除 current_app
        2.删除测试数据库
        3.销毁 setup() 创建的环境
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """测试函数：测试app实例是否可以成功创建"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试函数：测试app实例配置加载"""
        self.assertTrue(current_app.config['TESTING'])
