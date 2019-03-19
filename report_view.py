#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from flask_sqlalchemy import Pagination
from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///report_data.db'

bootstrap = Bootstrap(app)
app.secret_key = 'development key'

report_db = SQLAlchemy(app)
report_db.init_app(app)


class UpdateItem(FlaskForm):
    log_id = TextField('log_id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    ami_id = TextField('ami_id', render_kw={'readonly': True})
    instance_type = TextField('instance_type', render_kw={'readonly': True})
    compose_id = TextField('compose_id', render_kw={'readonly': True})
    instance_available_date = TextField('instance_available_date')
    pkg_ver = TextField('pkg_ver', render_kw={'readonly': True})
    bug_id = TextField('bug_id')
    report_url = TextField('report_url')
    branch_name = TextField('branch_name')
    cases_pass = TextField('cases_pass', render_kw={'readonly': True})
    cases_fail = TextField('cases_fail', render_kw={'readonly': True})
    cases_cancel = TextField('cases_cancel', render_kw={'readonly': True})
    cases_other = TextField('cases_other', render_kw={'readonly': True})
    cases_total = TextField('cases_total', render_kw={'readonly': True})
    pass_rate = TextField('pass_rate', render_kw={'readonly': True})
    test_date = TextField('test_date', render_kw={'readonly': True})
    comments = TextAreaField('comments')
    submit = SubmitField("Update")


class LoginForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    submit = SubmitField("Login")


class User(report_db.Model):
    __tablename__ = 'user_info'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    sqlite_autoincrement = True


class Report(report_db.Model):
    __tablename__ = 'report_info'

    log_id = Column(Integer, primary_key=True)
    ami_id = Column(String)
    instance_type = Column(String)
    compose_id = Column(String)
    instance_available_date = Column(String)
    pkg_ver = Column(String)
    bug_id = Column(String)
    report_url = Column(String)
    branch_name = Column(String)
    cases_pass = Column(Integer)
    cases_fail = Column(Integer)
    cases_cancel = Column(Integer)
    cases_other = Column(Integer)
    cases_total = Column(Integer)
    pass_rate = Column(Integer)
    test_date = Column(String)
    comments = Column(String)
    sqlite_autoincrement = True


@app.route('/', methods=['GET', 'POST'])
def home():
    per_page_default = 50

    reports = Report.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)
    query_filed = request.args.get('search_input')
    query_item = request.args.get('select_item')
    clear_session = request.args.get('clear', 0, type=int)
    if clear_session == 1:
        if session.has_key('username'):
            username = session['username']
            session.clear()
            session['username'] = username
        else:
            session.clear()

        query_obj = None
    else:
        if query_item is None and session.has_key("query_item"):
            query_item = session['query_item']
            query_filed = session['query_filed']
        elif query_item is not None:
            session['query_item'] = query_item
            session['query_filed'] = query_filed
        try:
            if 'ami_id' in query_item:
                query_obj = Report.ami_id
            elif 'instance_type' in query_item:
                query_obj = Report.instance_type
            elif 'instance_available_date' in query_item:
                query_obj = Report.instance_available_date
            elif 'compose_id' in query_item:
                query_obj = Report.compose_id
            elif 'pkg_ver' in query_item:
                query_obj = Report.pkg_ver
            elif 'bug_id' in query_item:
                query_obj = Report.bug_id
            elif 'branch_name' in query_item:
                query_obj = Report.branch_name
            elif 'test_date' in query_item:
                query_obj = Report.test_date
            else:
                query_obj = None
        except Exception as err:
            query_obj = None
        # print("%s-%s-%s" % (query_filed, query_item, session['query_item']))

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page

    if query_obj is not None:
        filter_item = query_obj.like("%"+query_filed+"%")
        pagination = Report.query.filter(or_(filter_item)).order_by(
            Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
    else:
        pagination = Report.query.order_by(
            Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)

    # pagination = Report.query.order_by(
    #    Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
    # posts = pagination.items
    reports = pagination.items
    # if session['per_page'] > 5:
    #    url_for('home', per_page=session['per_page'])
    return render_template('home.html', per_page=session['per_page'], reports=reports, pagination=pagination, query_item=query_item, query_filed=query_filed)


@app.route('/update_item', methods=['GET', 'POST'])
def update_item():

    item_form = UpdateItem()
    log_id = request.args.get('log_id', 0, type=int)
    if log_id != 0:
        session['log_id'] = log_id
    elif log_id == 0:
        log_id = session['log_id']
    try:
        login_form = LoginForm()
        if session['username'] == None:
            return render_template('login.html', form=login_form)
    except KeyError as err:
        return render_template('login.html', form=login_form)
    if request.method == 'GET':
        report_list = Report.query.filter(Report.log_id == log_id).all()
        print(report_list[0].ami_id)
        item_form.log_id.data = log_id

        item_form.ami_id.data = report_list[0].ami_id
        item_form.instance_type.data = report_list[0].instance_type
        item_form.compose_id.data = report_list[0].compose_id
        item_form.instance_available_date.data = report_list[0].instance_available_date
        item_form.pkg_ver.data = report_list[0].pkg_ver
        item_form.bug_id.data = report_list[0].bug_id
        item_form.report_url.data = report_list[0].report_url
        item_form.branch_name.data = report_list[0].branch_name
        item_form.cases_pass.data = report_list[0].cases_pass
        item_form.cases_fail.data = report_list[0].cases_fail
        item_form.cases_cancel.data = report_list[0].cases_cancel
        item_form.cases_other.data = report_list[0].cases_other
        item_form.cases_total.data = report_list[0].cases_total
        item_form.pass_rate.data = report_list[0].pass_rate
        item_form.test_date.data = report_list[0].test_date
        item_form.comments.data = report_list[0].comments
        return render_template('update_item.html', form=item_form)
    if request.method == 'POST':
        print(item_form.comments.data)

        try:
            report = Report.query.filter(Report.log_id == log_id).first()
            report.comments = item_form.comments.data

            report_db.session.commit()
            msg = "Saved successfully!"
        except Exception as err:
            msg = "Saved failed!"
        flash(msg, 'warning')

        Report.query.filter(Report.log_id == log_id)
        item_form.log_id.data = log_id
        report_list = Report.query.filter(Report.log_id == log_id).all()
        item_form.ami_id.data = report_list[0].ami_id
        item_form.instance_type.data = report_list[0].instance_type
        item_form.compose_id.data = report_list[0].compose_id
        item_form.instance_available_date.data = report_list[0].instance_available_date
        item_form.pkg_ver.data = report_list[0].pkg_ver
        item_form.bug_id.data = report_list[0].bug_id
        item_form.report_url.data = report_list[0].report_url
        item_form.branch_name.data = report_list[0].branch_name
        item_form.cases_pass.data = report_list[0].cases_pass
        item_form.cases_fail.data = report_list[0].cases_fail
        item_form.cases_cancel.data = report_list[0].cases_cancel
        item_form.cases_other.data = report_list[0].cases_other
        item_form.cases_total.data = report_list[0].cases_total
        item_form.pass_rate.data = report_list[0].pass_rate
        item_form.test_date.data = report_list[0].test_date
        item_form.comments.data = report_list[0].comments
        return render_template('update_item.html', form=item_form, msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        login_form = LoginForm()
        if session['username'] != None:
            return redirect(url_for('home'))
    except KeyError as err:
        msg = 'Not login'
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=login_form, msg=msg)
    if request.method == 'POST':
        username = login_form.username.data
        password = login_form.password.data
        #print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        #print("%s:%s:%s" % (username, password, generate_password_hash('redhat')))
        hs = generate_password_hash('redhat')
        if check_password_hash(hs, 'redhat'):
            print('ok')
        else:
            print('fail')

        try:
            user = User.query.filter(User.username == username).first()
        except Exception as err:
            msg = 'Cannot get user info!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        if user == None:
            msg = 'Cannot get user info!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        #hash_password = generate_password_hash(password)
        if not check_password_hash(user.password, password):
            msg = 'Password not correct!'
            flash(msg, 'warning')
            return render_template('login.html', form=login_form)
        else:
            session['username'] = username
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
    # app.run(debug = True)
