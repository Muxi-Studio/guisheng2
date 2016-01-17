# coding: utf-8
"""
    test_client.py
    ~~~~~~~~~~~~~~

        使用测试客户端，模拟客户端的请求，发送功能
"""

import unittest
from flask import url_for
from app import create_app, db
from app.models import Role, User


class FlaskClientTestCase(unittest.TestCase):
    """flask 测试客户端"""
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # create test account
        u = User(
            email = 'test@test.com',
            password = 'test',
            username = 'test'
        )
        db.session.add(u)
        db.session.commit()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage(self):
        """test home_page"""
        response = self.client.get(url_for('main.index'))
        self.assertTrue('登录' in response.get_data(as_text=True))
        self.assertFalse('新闻' in response.get_data(as_text=True))

    def test_login(self):
        """test login_page"""
        response = self.client.post(url_for('auth.login'), data={
            'email':'test@test.com',
            'password':'test'
        }, follow_redirects = True)
        data = response.get_data(as_text=True)
        self.assertTrue('原创' in data)
