# -*- coding:UTF-8 -*-
# !/usr/bin/python

from flask import Blueprint

main = Blueprint('main', __name__,static_folder="/root/www/guisheng2/app/static")

from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
