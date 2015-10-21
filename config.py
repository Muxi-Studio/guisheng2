# -*- coding: UTF-8 -*-

"""
    config.py
    ~~~~~~~~~

        桂声后台配置文件
        1:邮件配置
        2:分页配置
        3:开发、测试、生产环境下的数据库配置
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    基本配置类
        1.  密钥配置
        2.　数据库回滚设置
        3.  邮件配置
        4.  分页配置
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I hate flask'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'webwebpy@163.com'
    MAIL_PASSWORD = os.environ.get("GUISHENG_MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = '[快乐的桂声后台]'
    FLASKY_MAIL_SENDER = '桂声管理员 <webwebpy@163.com>'
    FLASKY_ADMIN = 'webwebpy@163.com'
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发环境数据库配置"""
    DEBUG = True  # 调试器开启
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """测试环境数据库配置"""
    TESTING = True # 调试模式
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    """生产环境数据库配置"""
    DEBUG = False  # 生产环境下严禁开启调试器
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
     # 配置字典
    'development': DevelopmentConfig,
    'testing':     TestingConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig
}
