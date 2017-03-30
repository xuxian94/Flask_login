#!/usr/bin/python
# -*- coding:utf8 -*-

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
# 登录root
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/text2'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True