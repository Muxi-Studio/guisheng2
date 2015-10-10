# coding: utf-8

"""
    test_post_model.py
    ~~~~~~~~~~~~~~~~~~~~~~

        测试文章数据库模型
"""

from test_models_base import TestBaseModel
from app import create_app, db
from app.models import NewsPost, OriginsPost, IntersPost


class NewsPostTestCase(TestBaseModel):
    """继承TestBaseModel类，直接进行测试"""
    def test_newspost(self):
        """testing ---> model NewsPost, nothing have to test!"""
        pass

