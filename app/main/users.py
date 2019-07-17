
from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_

from forms import LoginForm, SearchForm, UpdateItemForm,NewUserForm,EditUserForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2
from .db_class import ProjectMap,AppUser,UserMixin

@login_manager.user_loader
def load_user(username):
    return AppUser.query.get(int(username))

@main.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        # print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        hs = generate_password_hash('redhat')
        if check_password_hash(hs, 'redhat'):
            print('ok')
        else:
            print('fail')

        try:
            user = AppUser.query.filter(AppUser.username == username).first()
        except Exception as err:
            msg = 'Cannot get user info!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        if user == None:
            msg = 'Cannot get user info!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        # hash_password = generate_password_hash(password)
        if not check_password_hash(user.password, password):
            msg = 'Password not correct!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        else:
            # user1 = User.query.get(login_form.username.data)
            login_user(user)

            return redirect(url_for('main.index'))
    else:
        msg = 'Not login'
        return render_template('login.html', form=login_form, msg=msg)


@main.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('You are not admin user!')
        return redirect(url_for('main.index'))
    user_form = NewUserForm()
    new_user = AppUser()
    msg=''
    if user_form.validate_on_submit():
        new_user.username = user_form.username.data
        password = user_form.password.data
        if AppUser.query.filter_by(username=new_user.username ).count() > 1:
                flash('User name already exists! %s ' % new_user.username ,'error')
                return render_template('add_user.html',form=user_form)
        # print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        # print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        new_user.password = generate_password_hash(password)
        new_user.email = user_form.email.data
        new_user.role = user_form.role.data
        report_db.session.add(new_user)
        report_db.session.commit()
        flash('Add user successfully %s ' % new_user.username ,'info')
        return redirect(url_for('main.login'))
    return render_template('add_user.html',form=user_form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')