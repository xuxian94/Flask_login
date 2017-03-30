#!/usr/bin/python
# -*- coding:utf8 -*-
import uuid

from flask import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

PROFILE_FILE = "profiles.json"    # 定义json文件存储用户名 密码

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """saver user name ,id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE,'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            print self.id+'11111111111'
            print self.password_hash+'22222222'

            profiles[self.username] = [self.password_hash,
                                       self.id]
            f.write(json.dumps(profiles))


    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash,password)


    def get_password_hash(self):
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username,None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
            return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        print user_id
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                print '1111111111'
                user_profiles = json.load(f)
                for user_name ,profile in user_profiles.iteritems():
                    print profile[1]+'222222222'
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None