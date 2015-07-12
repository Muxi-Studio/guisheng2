<<<<<<< HEAD
from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
=======
# -*- coding: UTF-8 -*- 
#!/usr/bin/python
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

#500错误一般都需要自定义错误界面，因为500错误是程序自身错误或服务器错误
#页面返回的信息是html代码，体验不够好，所以需要自定义错误界面。
@main.app_errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'),500


>>>>>>> 812ef9225c453d817622a7df6aa9786b7e2a9b77
