# coding: UTF-8

"""
    manage.py
    ~~~~~~~~~
    桂声APP管理文件
    1.app对象创建
    2.数据库管理
        1>数据库迁移: python manage.py db init; python manage.py db migrate -m "#"
        2>数据库更新: python manage.py db upgrade
        3>虚拟数据创建:　python manage.py shell
                        >>>User.generate_fake(100)
                        >>>NewsPost.generate_fake(100)
                        >>>OriginsPost.generate_fake(100)
                        >>>IntersPost.generate_fake(100)
    3.shell管理(默认导入)
        python manage.py shell
    4.用户管理
        添加用户
        python manage.py adduser user_email username
        password:
    5.测试
        python manage.py test (--coverage)
"""

import os
from app import create_app, db
from app.models import User, Role, Permission, NewsPost, OriginsPost, \
        IntersPost, NewsComment, OriginsComment, IntersComment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import sys


# 将默认编码改为utf-8, 避免乱码
reload(sys)
sys.setdefaultencoding('utf-8')


# 添加测试覆盖率
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')  # 覆盖分支以及app下的所有文件
    COV.start()


# 定义覆盖后再创建app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Permission=Permission,
        NewsPost=NewsPost,
        OriginsPost=OriginsPost,
        IntersPost=IntersPost,
        NewsComment=NewsComment,
        OriginsComment=OriginsComment,
        IntersComment=IntersComment
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """运行单元测试
       输出测试覆盖率报告"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        # os.execvp: 执行$PATH下的可执行文件
        # sys.executable: /usr/bin/python
        # sys.argv: ['manage.py', 'shell']
        # os.execvp('/usr/bin/python',['/usr/bin/python' 'manage.py', 'shell']
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print 'Coverage Summary:'
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, '/tmp/coverage')
        COV.html_report(directory=covdir)
        print 'HTML version: file://%s/index.html' % covdir
        COV.erase()


@manager.command
def adduser(email, username):
    """添加用户"""
    from getpass import getpass
    password = getpass('password: ')
    confirm = getpass('confirm: ')
    if password == confirm:
        user = User(
            email=email,
            username=username,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return "user %s add in database" % username
    else:
        return "密码不匹配"
        sys.exit(0)


if __name__ == '__main__':
    manager.run()
