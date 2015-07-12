<<<<<<< HEAD
from flask import Blueprint

main = Blueprint('main', __name__,static_folder="/root/www/guiSheng/flasky2/app/static")

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
=======
# -*- coding: UTF-8 -*- 
#!/usr/bin/python
from flask import Blueprint
#蓝图的创建(2个参数：1：蓝图的名字；2：蓝图所在的模块和包)
main = Blueprint('main',__name__)

from . import views,errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
>>>>>>> 812ef9225c453d817622a7df6aa9786b7e2a9b77
