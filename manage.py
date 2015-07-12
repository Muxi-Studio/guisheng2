# -*- coding: UTF-8 -*-
# !/usr/bin/python
"""
    manage.py
    ~~~~~~~~~
    桂声APP管理文件
    1.app对象创建
    2.数据库管理
        1>数据库迁移: python manage.py db init; python manage.py db migrate -m "#"
        2>数据库更新: python manage.py db upgrade
        3>虚拟数据创建：　python manage.py shell
                        >>>User.generate_fake(100)
                        >>>NewsPost.generate_fake(100)
                        >>>OriginsPost.generate_fake(100)
                        >>>IntersPost.generate_fake(100)
    3.shell管理
        python manage.py shell
"""

import os
from app import create_app, db
from app.models import User, Role, Permission, NewsPost, OriginsPost, IntersPost, NewsComment, OriginsComment, IntersComment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

#-------------------编码设置---------------------------
# html文件
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#------------------------------------------------------

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
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
