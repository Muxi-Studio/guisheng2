# coding: utf-8

"""
    test_api.py
    ~~~~~~~~~~~

        测试桂声API
"""

import unittest
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models import Role


class APITestCase(unittest.TestCase):
    """API 测试类"""
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # do not need cookie, this is restful
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        """basic Authorization & base 64 编码"""
        return {
            'Authorization':
                'Basic' + b64encode(
                    (username + ':' + password).encode('utf-8')
                ).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        """test no auth, just get"""
        response = self.client.get(url_for('api.get_news'), content_type='application/json')
        self.assertTrue(response.status_code == 200)

    def test_create_user(self):
        """test: use api to create a user"""


    def test_create_news(self):
        """test: use api to create a news"""
