# -*- coding: UTF-8 -*-
# !/usr/bin/python
"""
    forms.py
    ~~~~~~~~
        表单类文件
"""

from flask.ext.wtf import Form
from flaskckeditor import CKEditor
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required
from ..models import Role, User


class PostForm(Form, CKEditor):
    """提交表单类"""
    title = PageDownField(validators=[Required()])
    body = TextAreaField(validators=[Required()])
    submit = SubmitField('提交')


class CommentForm(Form):
    """评论表单类"""
    body = StringField('>>', validators=[Required()])
    submit = SubmitField('提交')
