# -*- coding: UTF-8 -*-
# !/usr/bin/python

"""
    models.py
    ~~~~~~~~~

        桂声app数据库文件
        author: neo1218
        from: muxi studio
        licence: MIT
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from . import db, login_manager
from markdown import markdown
from app.exceptions import ValidationError
from flask.ext.login import UserMixin, AnonymousUserMixin
import bleach
# 实现 flask-login 的默认方法
# is_authenticated(): 如果用户已经登录返回 True，否则返回 False
# is_active(): 如果允许用户登录返回 True, 否则返回 False, 禁用用户账户返回 False
# is_anonymous(): 对普通用户必须返回 False
# get_id(): 必须返回用户的唯一标识符，使用 Unicode 字符串


class Permission:
    """
    用户权限类 => 权限表:
        (16进制的用户表示法)
        1.COMMENT 评论权限
        2.WRITE_ARTICLES 写文章权限
        3.MODERATE_COMMENT 删除评论的权限
        4.ADMINISTER 管理员权限
    """
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    """ 用户角色类 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """
        插入角色
            1.User: 可以评论、写文章 true(默认)
            2.Moderator: 可以评论写文章,删除评论
            3.Administer: 管理员
        """
        roles = {
                'User' : (
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES,
                    True),
                'Moderator' : (
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES |
                    Permission.MODERATE_COMMENTS,
                    False),
                'Administrator' : (0xff, False)
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """ 用户类 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(164), unique=True, index=True)
    avatar_url = db.Column(db.String(164), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    news = db.relationship('NewsPost', backref="author", lazy="dynamic")
    origins = db.relationship("OriginsPost", backref="author", lazy="dynamic")
    inters = db.relationship("IntersPost", backref="author", lazy="dynamic")
    news_comment = db.relationship('NewsComment', backref="author", lazy="dynamic")
    origins_comment = db.relationship('OriginsComment', backref="author", lazy="dynamic")
    inters_comment = db.relationship('IntersComment', backref="author", lazy="dynamic")

    def __init__(self, **kwargs):
        """ 设置用户权限 """
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['GUISHENGAPP_ADMIN']:
                # admin root
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                # default user
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        """ 无法读取password原始值 """
        raise AttributeError('无法读取密码明文!')

    @password.setter
    def password(self, password):
        """
        将用户输入的密码单向加密后存入数据库
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        将用户输入的密码进行加密,并与数据库中的密码密值进行比对
        """
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        """ 用户可以做什么 """
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """ 确定用户是不是管理员 """
        return self.can(Permission.ADMINISTER)

    def generate_auth_token(self, expiration):
        """ 生成验证token:验证字段id """
        s = Serializer(
                current_app.config["SECRET_KEY"],
                expiration
                )
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        """ 验证token, 获取用户 """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        """API 以json格式[提、存]数据"""
        json_user = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar_url': self.avatar_url
            }
        return json_user

    @staticmethod
    def from_json(json_user):
        """ 更新自request_body """
        return User(
                username = json_user.get('username'),
                email = json_user.get('email'),
                password = json_user.get('password'),
                avatar_url = json_user.get('avatar_url')
            )

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    """用户回调函数: 根据 user_id 返回 user 对象"""
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    """
    AnonymousUser类:

        匿名类
        如果用户没有注册是允许(山民访问)
    """
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def __repr__(self):
        return "<AnonymousUser>"

login_manager.anonymous_user = AnonymousUser


class NewsPost(db.Model):
    """
        新闻文章类:
            id: 主键
            title: 标题
            body_html: 文章内容的html格式
            body: 文章内容
            timestamp: 时间戳
            author_id: 作者
            comments: 属性 新闻文章的评论
    """
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body_html = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("NewsComment", backref="news", lazy="dynamic")

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        使用bleach clean用户输入的markdown
        ========  以及自动链接url ========
        """
        allowed_tags = [
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'img'
                ]
        target.body_html = bleach.linkify(
                bleach.clean(
                    markdown(value, output_format='html'),
                    tags=allowed_tags, strip=True
                    )
                )

    def to_json(self):
        """ 将文章数据资源转换为json格式 """
        json_news = {
            'id': self.id,
            'title': self.title,
            'content': self.body_html,
            # 'body_html': self.body_html,
            'writer': url_for("api.get_user", id=self.author_id, _external=True),
            'date': self.timestamp
        }
        return json_news

    @staticmethod
    def from_json(json_news):
        body = json_news.get('body')
        if body is None or body == '':
            raise ValidationError('文章没有内容哦!')
        return NewsPost(body=body)

    def __repr__(self):
        return "<NewsPost %r>" % (self.id)

db.event.listen(NewsPost.body, 'set', NewsPost.on_changed_body)


class OriginsPost(db.Model):
    """
        OriginsPost类

            原创板块类(不仅仅只有文章)
            id: 主键
            title: 标题
            body_html: 文章内容的html格式
            body: 文章内容
            timestamp: 时间戳
            author_id: 作者
            comments: 属性 原创文章的评论
    """
    __tablename__ = "origins"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)  # 给了很大的空间(汉子占用字节大)
    body_html = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("OriginsComment", backref="origins", lazy="dynamic")  # backref的值待定(评论在这里比较特殊)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        markdown 文本框中允许使用的html标签
        用户插入的一些html标签可能是不安全的
        """
        allowed_tags = [
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'img'
                ]
        # 自动过滤其余标签
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        """json 格式的资源"""
        json_origins = {
            'id': self.id,
            'title': self.title,
            'content': self.body,
            # 'body_html': self.body_html,
            'writer': url_for("api.get_user", id=self.author_id, _external=True),
            'date': self.timestamp
        }
        return json_origins

    @staticmethod
    def from_json(json_origins):
        body = json_origins.get('body')
        if body is None or body == '':
            raise ValidationError('文章没有内容哦!')
        return OriginsPost(body=body)

db.event.listen(OriginsPost.body, 'set', OriginsPost.on_changed_body)


class IntersPost(db.Model):
    """
        IntersPost类

            互动板块类(不仅仅只有文章)
            id: 主键
            title: 标题
            body_html: 文章内容的html格式
            body: 文章内容
            timestamp: 时间戳
            author_id: 作者
            comments: 属性 互动文章的评论
    """
    __tablename__ = "inters"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)  # 给了很大的空间(汉子占用字节大)
    body_html = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("IntersComment", backref="inters", lazy="dynamic")  # backref的值待定(评论在这里比较特殊)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        markdown 文本框中允许使用的html标签
        用户插入的一些html标签可能是不安全的
        """
        allowed_tags = [
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'img'
                ]
        # 自动过滤其余标签
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        """json 格式的资源"""
        json_inters = {
            'id': self.id,
            'title': self.title,
            'content': self.body,
            # 'body_html': self.body_html,
            'writer': url_for("api.get_user", id=self.author_id, _external=True),
            'date': self.timestamp
            }
        return json_inters

    @staticmethod
    def from_json(json_inters):
        body = json_inters.get('body')
        if body is None or body == '':
            raise ValidationError('文章没有内容哦!')
        return IntersPost(body=body)

db.event.listen(IntersPost.body, 'set', IntersPost.on_changed_body)


class NewsComment(db.Model):
    """ 新闻评论类 """
    __tablename__ = 'newsComments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        过滤不安全的html标签
        自动链接url
        """
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_newsComment = {
                'id': self.id,
                'comment': self.body,
                'date': self.timestamp,
                'username': User.query.get_or_404(self.author_id).username,
                'avatar': User.query.get_or_404(self.author_id).avatar_url
                }
        return json_newsComment

    @staticmethod
    def from_json(json_newsComment):
        body = json_newsComment.get('comment')
        if body is None or body == '':
            raise ValidationError('comment can not be empty! ')
        return NewsComment(body=body)

db.event.listen(NewsComment.body, 'set', NewsComment.on_changed_body)


class OriginsComment(db.Model):
    """
    OriginsComment类:

        原创评论类
        id: 主键
        body: 原创评论的内容
        body_html: 原创评论的html形式
        timestamp: 时间戳
        disabled: ？什么时候会用到布尔值？？
        author_id: 作者的id
        news_id: 此评论对应的原创文章的id
    """
    __tablename__ = 'originsComments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    origins_id = db.Column(db.Integer, db.ForeignKey('origins.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """过滤html标签"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_originsComment = {
            'id': self.id,
            'comment': self.body,
            'date': self.timestamp,
            'avatar': User.query.get_or_404(self.author_id).avatar_url,
            'username': User.query.get_or_404(self.author_id).username
            }
        return json_originsComment

    @staticmethod
    def from_json(json_originsComment):
        body = json_originsComment.get('comment')
        if body is None or body == '':
            raise ValidationError('comment can not be empty')
        return OriginsComment(body=body)

db.event.listen(OriginsComment.body, 'set', OriginsComment.on_changed_body)


class IntersComment(db.Model):
    """
    IntersComment类:

        互动评论类
        id: 主键
        body: 互动评论的内容
        body_html: 互动评论的html形式
        timestamp: 时间戳
        disabled: ？什么时候会用到布尔值？？
        author_id: 作者的id
        inters_id: 此评论对应的互动文章的id
    """
    __tablename__ = 'intersComments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    inters_id = db.Column(db.Integer, db.ForeignKey('inters.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """过滤html标签"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_intersComment = {
            'id': self.id,
            'comment': self.body,
            'date': self.timestamp,
            'username': User.query.get_or_404(self.author_id).username,
            'avatar': User.query.get_or_404(self.author_id).avatar_url
            }
        return json_intersComment

    @staticmethod
    def from_json(json_intersComment):
        body = json_intersComment.get('comment')
        if body is None or body == '':
            raise ValidationError('comment can not be empty')
        return IntersComment(body=body)

db.event.listen(IntersComment.body, 'set', IntersComment.on_changed_body)
