# -*- coding: UTF-8 -*-
# !/usr/bin/python
"""
    views.py
    ~~~~~~~~

    auth登录模块视图函数文件
    由于桂声是一个面向编辑的后台网站，
    所以无需注册接口。账号直接由管理员发放。
"""
from flask import render_template
from flask import redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.login import current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm
# from .forms import RegistrationForm
from .forms import ResetForm


@auth.route('/login',methods=['GET','POST'])
def login():
    """登录界面视图函数"""
    form = LoginForm()
    if form.validate_on_submit():  # POST
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)  # flask-login
			return redirect(request.args.get('next') or url_for('main.index'))
		flash("用户名或密码不存在")
    return render_template('auth/login.html', form=form)  # GET


@auth.route('/logout')
@login_required
def logout():
    """退出界面视图函数"""
    logout_user()  # flask-login
    flash("你已退出")
    return redirect(url_for("main.index"))


@login_required
@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    """url='/reset', 　重置用户密码"""
    form = ResetForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password1.data
            db.session.add(current_user)
            flash('密码已经更新!')
            return redirect(url_for('main.index'))
        else:
            flash('旧密码输入有错！')
    return render_template('auth/change_password.html', form=form)
