# coding: utf-8

from flask import Blueprint

<<<<<<< HEAD
main = Blueprint('main', __name__,static_folder="/root/guisheng2/app/static") # static_folder: 静态文件存储目录
=======
main = Blueprint(
    'main',
    __name__,
    template_folder = 'templates',
    static_folder = '/root/www/guishengapp/app/static'
)
>>>>>>> 42ca2786107ed5086652c88cd129d4ac46084221

from . import views, forms
