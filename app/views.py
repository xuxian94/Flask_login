#!/usr/bin/python
# -*- coding:utf8 -*-
import os

from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_wtf import CSRFProtect
from models import LoginForm
from models import User
from app import app
app.secret_key = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'  # 未登录用户重定向到login
login_manager.init_app(app)

# callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(id):
    return User.get(id)

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)


        user = User(user_name)
        if user.verify_password(password):
            login_user(user)
            return redirect(url_for('main'))
    return render_template('login1.html',title="Sign In",form=form)


@app.route('/')
@app.route('/main')
@login_required
def main():
    return render_template(
        'main.html'
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)