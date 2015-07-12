# -*- coding: UTF-8 -*-
# !/usr/bin/python
# uwsgi服务器启动文件
from manage import app


if __name__ == "__main__":
	app.run(host="121.43.230.104",port = 5000)
