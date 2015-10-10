# coding: UTF-8

"""
    test_user_model.py
    ~~~~~~~~~~~~~~~~~~

        测试用户模型
"""
import unittest
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        创建测试实例、程序上下文、数据库
        添加 Role 角色
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        """
        销毁楼上的一切
        db.session.add()
        db.session.commit()
        db.session.delete()
        db.session.remove()
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        """testing ---> generate password to password_hash"""
        u = User(password='test')
        # assertTrue 假定正确, 若正确返回True，否则返回False
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        """tesing ---> can not read the raw password"""
        u = User(password='test')
        with self.assertRaises(AttributeError):
            # 希望触发 AttributeError
            u.password

    def test_password_verification(self):
        """testing ---> cat is not equal to dog !😄  """
        # assert is hope !
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        """testing ---> password salts are random ! and salts is important!"""
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        """testing ---> roles and permissions"""
        u1 = User(email='john@example.com', password='cat')
        u2 = User(email='webwebpy@163.com', password='1234')
        # test normal user
        self.assertTrue(u1.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u1.can(Permission.MODERATE_COMMENTS))
        # test the admin user
        self.assertTrue(u2.can(Permission.WRITE_ARTICLES))
        self.assertTrue(u2.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        """testing ---> anonymous user"""
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.WRITE_ARTICLES))
