# -*- coding: UTF-8 -*-
# !/usr/bin/python
from flask import render_template
from flask import redirect,request,url_for,flash
from flask.ext.login import login_user,login_required,logout_user
from flask.ext.login import current_user

from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm
from .forms import RegistrationForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.uncofirmed'))

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash("用户名或密码不存在")
	return render_template('auth/login.html',form=form)


@auth.route('/logout')

@login_required
def logout():
	logout_user()
	flash("你已退出")
    return redirect(url_for("main.index"))


@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
		db.session.add(user)
		flash('注册成功，现在可以登陆了')
		return redirect(url_for('auth.login'))
		db.session.add(user)
		db.session.commit()
		token=user.generate_confirmation_token()
		send_email(user.email,'请确认你的账户',
                    'auth/email/confirm',user=user,token=token)
		flash('确认账户的邮件已发送！')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')

@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('你已经确认了账户，谢谢！')
	else:
		flash('先确认你的账户吧！')
	return redirect(url_for('main.index'))

@auth.route('confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,'请确认你的账户',
                'auth/email/confirm',user=current_user,token=token)
	flash('一个新的确认邮件已发送！')
	return redirect(url_for('main.index'))



@auth.route('/uncofirmed')
def uncofirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

