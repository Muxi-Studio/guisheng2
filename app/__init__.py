# -*- coding: UTF-8 -*-
#!/usr/bin/python

"""
	__init__.py
	~~~~~~~~~~~

		app　包初始化文件
		1. 将 app 包作为模块导入
		2. 初始化
		3. 蓝图注册
"""

import os
import re
import json
import random
import urllib
import datetime
from flask import Flask ,render_template,request,url_for,make_response
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.pagedown import PageDown
from config import config


# flask扩展实例化
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # None, basic, strong
login_manager.login_view = 'auth.login'  # endpoint of auth


# 文件上传函数
def gen_rnd_filename():
	#以文件上传的日期确定文件名
	filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	return "%s%s" % (filename_prefix,str(random.randrange(1000,10000)))


def create_app(config_name):
	"""创建 app 实例工厂函数
	　　
	  1. 创建 app 实例:
	  app = Flask(__name__)

	  2. 加载初始化配置：
	　 app.config.from_object(config_name)
	  config[config_name].init_app(app)

	  3. 各个扩展对象的初始化:
	  bootstrap mail moment db login_manager

	  4. 蓝图注册：
	　from .[] import [] as []_blueprint
	  app.register_blueprint([]_blueprint, url_prefix=urls)"""

	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
    	from .main import main as main_blueprint
    	app.register_blueprint(main_blueprint)

    	from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint,url_prefix='/auth')

    	from .api_1_0 import api as api_1_0_blueprint
    	app.register_blueprint(api_1_0_blueprint,url_prefix='/api/v1.0')

    	return app
