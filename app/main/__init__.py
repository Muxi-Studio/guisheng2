# coding: utf-8

from flask import Blueprint

main = Blueprint(
    'main',
    __name__,
    template_folder = 'templates',
    static_folder = '/root/www/guishengapp/app/static'
)

from . import views, forms
