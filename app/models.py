#!/usr/bin/python
# -*- coding:utf8 -*-


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from app import app
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@localhost:3306/text2' #这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True #设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app) #实例化

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class Login_Form(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<Login_Form {}'.format(self.username)

    def __init__(self,
                 username,
                 password):
        self.username = username
        self.password = password


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """saver user name ,id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        # with open(PROFILE_FILE,'w+') as f:
        #     try:
        #         profiles = json.load(f)
        #     except ValueError:
        #         profiles = {}
        #
        #     profiles[self.username] = [self.password_hash,
        #                                self.id]
        #     f.write(json.dumps(profiles))


        self.create_account()

    def verify_password(self, password):  # 认证密码
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def get_password_hash(self):
        try:
            # with open(PROFILE_FILE) as f:
            #     user_profiles = json.load(f)
            #     user_info = user_profiles.get(self.username,None)
            #     if user_info is not None:
            #         return user_info[0]

            user = select_sql(self.username)

            if user is not None:
                return user.password



        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        if self.username is not None:
            try:
                # with open(PROFILE_FILE) as f:
                #     user_profiles = json.load(f)
                #     if self.username in user_profiles:
                #         return user_profiles[self.username][1]

                # user = self.select_sql(self.username)
                user = select_sql(self.username)
                if user is not None:
                    return user.id
            except IOError:
                pass
            except ValueError:
                pass
            return None

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        try:
            # with open(PROFILE_FILE) as f:
            #     print '1111111111'
            #     user_profiles = json.load(f)
            #     for user_name ,profile in user_profiles.iteritems():
            #         print profile[1]+'222222222'
            #         if profile[1] == user_id:
            #             return User(user_name)

            # user = select_sql()
            user = Login_Form.query.filter_by(id = user_id).first()
            if user.id == user_id:
                return User(user.username)


        except:
            return None
        return None


def select_sql(username):
    if username is not None:
        try:
            userInfo = Login_Form.query.filter_by(username=username.encode('utf-8')).first()
            return userInfo
        except IOError:
            return None
        except ValueError:
            return None
        return None


def create_account(username, password_hash):
    account = Login_Form(username, password_hash)
    db.session.add(account)
    db.session.commit()


if __name__ == '__main__':
    user = select_sql('admin')
    print user.username
    print user.password

    # create_account('lisi',generate_password_hash('123456'))
