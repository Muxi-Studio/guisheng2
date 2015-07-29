# -*- coding: UTF-8 -*-
#!/usr/bin/python
"""
	forms.py
	~~~~~~~~

	登录模块表单
"""
from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, BooleanField, StringField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
	"""登录表单"""
	email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('密码', validators=[Required()])
	remember_me = BooleanField('记住我')
	submit = SubmitField('登录')


class RegistrationForm(Form):
	"""注册表单"""
	email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
	username = StringField('用户名')
	password = PasswordField('密码', validators=[Required(),EqualTo('password2', message="密码必须匹配")])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		"""验证邮箱是否已经注册"""
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已被注册')

	def validate_username(self,field):
		"""验证用户名是否已经注册"""
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已存在')



class ResetForm(Form):
    """重置密码表单类"""
    old_password =  PasswordField("输入旧密码:", validators=[Required()])
    password1 = PasswordField(
        "输入新密码", validators=[Required(),
        EqualTo('password2', message='密码必须匹配')]
    )
    password2 = PasswordField('确认新密码:', validators=[Required()])
    submit = SubmitField('更新')
