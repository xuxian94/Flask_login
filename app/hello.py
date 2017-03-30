#!/usr/bin/python
# -*- coding:utf8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import MySQLdb

app = Flask(__name__)
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@localhost:3306/text2' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app) #实例化

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.INTEGER,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    user = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __init__(self,
                 name):
        self.name = name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.INTEGER,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)



if __name__ == '__main__':

    #####################    生成mysql数据库        #################
    # db.create_all()
    # admin_role = Role(name='admin')  # 实例化
    # mod_role = Role(name='Moderator')
    # user_role = Role(name='User')
    # user_john = User(username='john', role=admin_role)  # role属性也可使用，虽然他不是真正的数据库列，但却是一对多关系的高级表示
    # user_susan = User(username='susan', role=user_role)
    # user_david = User(username='david', role=user_role)
    # db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan,
    #                     user_david])  # 准备把对象写入数据库之前，先要将其添加到会话中，数据库会话db.session和Flask session对象没有关系，数据库会话也称事物
    # db.session.commit()  # 提交会话到数据库


    #########################         删除       ###########################
    # name = Role.query.filter_by(name = 'Adminstrator').first()
    # db.session.delete(name)
    # db.session.commit()


    inset = Role(name='admin')
    db.session.add(inset)
    db.session.commit()