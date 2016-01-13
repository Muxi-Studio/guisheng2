# -*- coding: UTF-8 -*-

"""
	桂声app后台
	~~~~~~~~~~

	__init__.py
	~~~~~~~~~~~

		app　包初始化文件
		1. 将 app 包作为模块导入
		2. 初始化
		3. 蓝图注册

"""

from flask import Flask
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from config import config

config_name = 'default'

# Flask app
app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Flask exts
bootstrap = Bootstrap(app)
mail = Mail(app)
moment = Moment(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'  # None, basic, strong
login_manager.login_view = 'auth.login'

# Flask blueprint
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint,url_prefix='/auth')

from .api_1_0 import api as api_1_0_blueprint
app.register_blueprint(api_1_0_blueprint,url_prefix='/api/v1.0')
