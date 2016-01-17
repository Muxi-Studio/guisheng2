# coding: utf-8
from flask_wtf import Form
from flaskckeditor import CKEditor
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class LoginForm(Form):
    """登录表单"""
    email = StringField('邮箱', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('登录')


class EditForm(Form, CKEditor):
    """新闻,原创,互动编辑器(ckeditor)"""
    title = StringField('title', validators=[Required()])
    post = TextAreaField('post', validators=[Required()])
    submit = SubmitField('提交')

