# -*- coding: UTF-8 -*-
#!/usr/bin/python

"""
    models.py
    ~~~~~~~~~
        桂声app数据库文件
        author: neo1218
        from: muxi studio
        licence:
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from markdown import markdown
from app.exceptions import ValidationError
import hashlib
import bleach

class Permission:
    """
    Permission类:

        用户权限类
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
    """
    Role类:

        用户角色类
        id: 主键
        name: 角色的名字
        default: 默认角色
        permission: id 角色对应的权限
        users: 属性 反向查找user
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod # 静态方法,可以被类直接调用
    def insert_roles():
        """
        插入角色
            1.User: 可以评论、写文章 true(默认)
            2.Moderator: 可以评论写文章,删除评论
            3.Administer: 管理员(想干什么干什么)
            # 其实还有我: 直接操纵数据库:)
        """
# ***************************************************************
        roles = {
            'User': (Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role) # 添加进数据库
        db.session.commit() # 提交
# ****************************************************************
    def __repr__(self):
        """该类的'官方'表示方法"""
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    """
    User类:

        用户类
        id: 主键
        email: 用户的邮箱地址(此地址用于用户找回密码，无需进行邮箱验证)
        username: 用户名
        password_hash: 用户密码
        avatar: 头像(尚未完成)
        role_id: 指向用户角色的外键
        #post 这里的文章中可能包含图片,或者就是纯图片(图集)
        news: 属性 用户发布的新闻文章
        origins: 属性 用户发布的原创文章
        inters: 属性 用户发布的互动文章
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # avatar() = db.Column(pass)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128)) # password 是绝对不允许以明文的形式存储在数据库中的
    # posts = db.relationship('Post',backref="author",lazy="dynamic")
    news = db.relationship('NewsPost',backref="author",lazy="dynamic")
    origins = db.relationship("OriginsPost",backref="author",lazy="dynamic")
    inters = db.relationship("IntersPost",backref="author",lazy="dynamic")
    # comment
    news_comment = db.relationship('NewsComment',backref="author",lazy="dynamic")
    origins_comment = db.relationship('OriginsComment',backref="author",lazy="dynamic")
    inters_comment = db.relationship('IntersComment',backref="author",lazy="dynamic")

    @staticmethod
    def generate_fake(count=100):
        """添加100虚拟数据"""
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word()
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        """检查用户邮箱是否是环境变量设置的管理员邮箱,若是则管理员,否则是默认"""
        # 超类构造器(简化参数调用,不受Column的限制)
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
#***********************************************************************
    # 方便实例调用(属性比函数更直观)
    @property # python属性装饰器 将password编程属性
    def password(self):
        raise AttributeError('密码字符出错啦')

    @password.setter# @property生成setter装饰器,限定password
    def password(self, password):
        """
        对密码进行hash加密,加密的过程是单向的,用户输入得到相同的结果与数据库进行比对
            每当一个user新建时调用该函数
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        验证密码
            每当需要验证密码的时候调用该函数
        """
        return check_password_hash(self.password_hash, password)
# **********************************************************************
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        """允许用户修改email(防止用户注册的时候输错email)"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        """上次登录的时间(可选)"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self):
        """头像占位(不知道具体如何处理)"""
        pass

    def to_json(self):
        """API 以json格式[提、存]数据"""
        json_user = {
            'url': url_for('api.get_news', id=self.id, _external=True),
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen, # 可选
            'news': url_for('api.get_user_news', id=self.id, _external=True),
            'origins': url_for('api.get_user_origins',id=self.id, _external=True),
            'inters': url_for('api.get_user_inters',id=self.id, _external=True),
            'news_comment': url_for('api.get_user_news_comment', id=self.id, _external=True),
            'origins_comment': url_for("api.get_user_origins_comment", id=self.id, _external= True),
            'inters_comment': url_for("api.get_user_inters_comment", id=self.id, _external=True)
        }

    """
    token(令牌)是一种验证方式(一般和用户信息相关),他有寿命，我们只需在生成用户和密码时生成一个token和寿命期限,
    在验证token时,在寿命期限内,token会变成纯文本密码,然后与数据库中存储进行比对
    """
    def generate_auth_token(self, expiration):
        """用用户的id生成token"""
        s = Serializer(
                current_app.config["SECRET_KEY"],
                expires_in=expiration # token的寿命
            )
        return s.dumps({'id':self.id}).decode('ascii') # 去除ascii码,保存数据

    @staticmethod
    def verify_auth_token(token):
        """验证token"""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token) # 尝试加载token
        except:
            return None
        return User.query.get(data[id]) #User 是一个数据,query就是数据库查询函数

    def __repr__(self):
        """User类的官方字符串显示"""
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    """
    AnonymousUser类:

        匿名类
        如果用户没有注册是允许(山民访问)
    """
# ***************************************
    def can(self, permissions):
        return False
# ***************************************
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class NewsPost(db.Model):
    """
        NewsPost类

            新闻文章类
            id: 主键
            title: 标题
            body_html: 文章内容的html格式
            body: 文章内容
            timestamp: 时间戳
            author_id: 作者
            comments: 属性 新闻文章的评论
    """
    __tablename__ = "news"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))# 给了很大的空间(汉子占用字节大)
    body_html = db.Column()
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship("NewsComment", backref="news", lazy="dynamic") # backref的值待定(评论在这里比较特殊)

    @staticmethod
    def generate_fake(count=100):
        """生成新闻文章虚拟数据"""
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = NewsPost(
                    body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                    timestamp=forgery_py.date.date(True),
                    author=u
            )
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        markdown 文本框中允许使用的html标签
        用户插入的一些html标签可能是不安全的
        """
        allowed_tags = [
                'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3','h4','h5','h6','p','br','img'
        ]
        # 自动过滤其余标签
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        """json 格式的资源"""
        json_news = {
            'url' : url_for("api.get_news", id=self.id, _external=True),
            'title': self.title,
            'body': self.body,
            'body_html': self.body_html,
            'author': url_for("api.get_user", id=self.author_id, _external=True),
            'comments': url_for("api.get_news_comments", id=self.id, _external=True),
            'timestamp': self.timestamp
        }
        return json_news

    @staticmethod
    def from_json(json_news):
        body = json_news.get('body')
        if body is None or body == '':
            raise ValidationError('文章没有内容哦!')
        return NewsPost(body=body)

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
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))# 给了很大的空间(汉子占用字节大)
    body_html = db.Column()
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship("OriginsComment",backref="origins", lazy="dynamic")# backref的值待定(评论在这里比较特殊)

    @staticmethod
    def generate_fake(count=100):
        """
        生成原创板块虚拟数据
        由于生成的虚拟数据中并不包括图片,所以测试时需要自己上传图片到数据库中
        """
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = OriginsPost(
                    body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                    timestamp=forgery_py.date.date(True),
                    author=u
            )
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        markdown 文本框中允许使用的html标签
        用户插入的一些html标签可能是不安全的
        """
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3','h4','h5','h6','p','br','img'
        ]
        # 自动过滤其余标签
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        """json 格式的资源"""
        json_origins = {
            'url' : url_for("api.get_origins", id=self.id, _external=True),
            'title': self.title,
            'body': self.body,
            'body_html': self.body_html,
            'author': url_for("api.get_user",id=self.author_id,_external=True),
            'comments': url_for("api.get_origins_comments", id=self.id, _external=True),
            'timestamp': self.timestamp
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

            互动版块类
            id: 主键
            title: 标题
            body_html: 文章内容的html格式(可能包含图片,对于图片的处理依据文件名在存储文件夹中进行查找)
            body: 文章内容
            timestamp: 时间戳
            author_id: 作者
            comments: 属性 互动文章的评论
    """
    __tablename__ = "inters"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))# 给了很大的空间(汉子占用字节大)
    body_html = db.Column()
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship("IntersComment",backref="inters", lazy="dynamic")# backref的值待定(评论在这里比较特殊)

    @staticmethod
    def generate_fake(count=100):
        """生成互动板块的虚拟数据"""
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = IntersPost(
                    body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                    timestamp=forgery_py.date.date(True),
                    author=u
            )
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """
        markdown 文本框中允许使用的html标签
        用户插入的一些html标签可能是不安全的
        """
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3','h4','h5','h6','p','br','img'
        ]
        # 自动过滤其余标签
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        """json 格式的资源"""
        json_inters = {
            'url' : url_for("api.get_inters", id=self.id, _external=True),
            'title': self.title,
            'body': self.body,
            'body_html': self.body_html,
            'author': url_for("api.get_user",id=self.author_id,_external=True),
            'comments': url_for("api.get_inters_comments", id=self.id, _external=True),
            'timestamp': self.timestamp
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
    """
    NewsComment类:

        新闻评论类
        id: 主键
        body: 新闻评论的内容
        body_html: 新闻评论的html形式
        timestamp: 时间戳
        disabled: ？什么时候会用到布尔值？？
        author_id: 作者的id
        news_id: 此评论对应的新闻文章的id
    """
    __tablename__ = 'newsComments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean) # ??:(
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """过滤html标签"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_newsComment = {
            'url': url_for('api.get_newsComment', id=self.id, _external=True),
            'news': url_for('api.get_news', id=self.news_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
        }
        return json_newsComment

    @staticmethod
    def from_json(json_newsComment):
        body = json_newsComment.get('body')
        if body is None or body == '':
            raise ValidationError('评论不能为空哦!')
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
    disabled = db.Column(db.Boolean) # ??:(
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('origins.id'))

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
            'url': url_for('api.get_originsComment', id=self.id, _external=True),
            'news': url_for('api.get_origins', id=self.news_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
        }
        return json_originsComment

    @staticmethod
    def from_json(json_originsComment):
        body = json_originsComment.get('body')
        if body is None or body == '':
            raise ValidationError('评论不能为空哦!')
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
        news_id: 此评论对应的互动文章的id
    """
    __tablename__ = 'intersComments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean) # ??:(
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('inters.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        """过滤html标签"""
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_newsComment = {
            'url': url_for('api.get_intersComment', id=self.id, _external=True),
            'news': url_for('api.get_inters', id=self.news_id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
        }
        return json_intersComment

    @staticmethod
    def from_json(json_intersComment):
        body = json_intersComment.get('body')
        if body is None or body == '':
            raise ValidationError('评论不能为空哦!')
        return IntersComment(body=body)

db.event.listen(IntersComment.body, 'set', IntersComment.on_changed_body)
