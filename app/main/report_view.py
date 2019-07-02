
from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_

from forms import LoginForm, SearchForm, UpdateItemForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2
from flask_googlecharts import GoogleCharts, ColumnChart, BarChart, LineChart

from .db_class import ProjectMap

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


class User(report_db.Model):
    __tablename__ = 'user_info'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    sqlite_autoincrement = True

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.userid

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


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


@main.route('/', methods=['GET', 'POST'])
def home():
    per_page_default = 50
    search_form = SearchForm(csrf_enabled=True)
    msg = ''

    if search_form.validate_on_submit():
        if search_form.reset.data:
            msg += "Clear all filters!"
            # session.clear()
            session.pop('query_filed', None)
            session.pop('select_item', None)
            session.pop('query_item', None)
            query_obj = None
            return redirect(url_for('main.home'))
        else:
            query_filed = search_form.search_input.data
            query_item = search_form.select_item.data
    else:
        query_filed = request.args.get('query_filed')
        query_item = request.args.get('query_item')
    reports = Report.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)

    clear_session = request.args.get('clear', 0, type=int)
    find_count = 0
    find_count = Report.query.count()

    if query_item is None and session.has_key("query_item"):
        query_item = session['query_item']
        query_filed = session['query_filed']
        search_form.search_input.data = query_filed
        search_form.select_item.data = query_item
    elif query_item is not None:
        session['query_item'] = query_item
        session['query_filed'] = query_filed
        search_form.search_input.data = query_filed
        search_form.select_item.data = query_item
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

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page

    if query_obj is not None:
        filter_item = query_obj.like("%"+query_filed+"%")
        pagination = Report.query.filter(or_(filter_item)).order_by(
            Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
        find_count = Report.query.filter(or_(filter_item)).count()
    else:
        find_count = Report.query.count()
        pagination = Report.query.order_by(
            Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)

    # pagination = Report.query.order_by(
    #    Report.log_id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
    # posts = pagination.items
    reports = pagination.items
    # if session['per_page'] > 5:
    #    url_for('home', per_page=session['per_page'])
    msg += 'Found %s items!' % find_count

    if search_form.validate_on_submit():
        return redirect(url_for('main.home', query_item=query_item, query_filed=query_filed))
    flash(msg, category='info')
    return render_template('home.html', per_page=session['per_page'], form=search_form, reports=reports, pagination=pagination, query_item=query_item, query_filed=query_filed)

@main.route('/update_item', methods=['GET', 'POST'])
def update_item():

    item_form = UpdateItemForm()
    search_form = SearchForm(csrf_enabled=True)
    if search_form.validate_on_submit():
        if search_form.reset.data:
            msg += "Clear all filters!"
            # session.clear()
            session.pop('query_filed', None)
            session.pop('select_item', None)
            session.pop('query_item', None)
            query_obj = None
            return redirect(url_for('home'))
        else:
            query_filed = search_form.search_input.data
            query_item = search_form.select_item.data
        return redirect(url_for('home',query_filed=query_filed,query_item=query_item))
        

    log_id = request.args.get('log_id', 0, type=int)
    if log_id != 0:
        session['log_id'] = log_id
    elif log_id == 0:
        log_id = session['log_id']
        login_form = LoginForm()
    if not current_user.is_authenticated:
        flash('Not auth')
        return redirect(url_for('main.login'))
    msg = None
    if item_form.validate_on_submit():
        try:
            if item_form.delete.data:
                flash("Item %s deleted" % log_id)
                report = Report.query.filter(Report.log_id == log_id).first()
                report_db.session.delete(report)
                report_db.session.commit()
                return redirect(url_for('main.home'))
            report = Report.query.filter(Report.log_id == log_id).first()

            report.ami_id = item_form.ami_id.data
            report.instance_type = item_form.instance_type.data
            report.compose_id = item_form.compose_id.data
            report.instance_available_date = item_form.instance_available_date.data
            report.pkg_ver = item_form.pkg_ver.data
            report.bug_id = item_form.bug_id.data
            report.report_url = item_form.report_url.data
            report.branch_name = item_form.branch_name.data
            report.cases_pass = item_form.cases_pass.data
            report.cases_fail = item_form.cases_fail.data
            report.cases_cancel = item_form.cases_cancel.data
            report.cases_other = item_form.cases_other.data
            report.cases_total = item_form.cases_total.data
            report.pass_rate = item_form.pass_rate.data
            report.test_date = item_form.test_date.data
            report.comments = item_form.comments.data

            report_db.session.commit()
            msg = "Saved successfully!"
        except Exception as err:
            msg = "Saved failed!"
            print(err)
        flash(msg, 'warning')

    report_list = Report.query.filter(Report.log_id == log_id).all()
    if len(report_list) == 0:
        flash('No record found log_id: %s!' % log_id, 'warning')
        return redirect(url_for('main.home'))
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
    return render_template('update_item.html', form=search_form, item_form=item_form, msg=msg)


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
            user = User.query.filter(User.username == username).first()
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
            user.is_authenticated = True
            login_user(user)

            return redirect(url_for('main.home'))
    else:
        msg = 'Not login'
        return render_template('login.html', form=login_form, msg=msg)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@main.route('/show_chart', methods=['GET', 'POST'])
def show_chart():
    search_form = SearchForm(csrf_enabled=True)
    query_obj = None
    find_count = 0
    msg = ''
    if search_form.validate_on_submit():
        if search_form.reset.data:
            msg += "Clear all filters!"
            # session.clear()
            session.pop('query_filed', None)
            session.pop('select_item', None)
            session.pop('query_item', None)
            query_obj = None
            return redirect(url_for('main.show_chart'))
        else:
            query_filed = search_form.search_input.data
            query_item = search_form.select_item.data
    else:
        query_filed = request.args.get('search_input')
        query_item = request.args.get('select_item')
    if query_item is None and session.has_key("query_item"):
        query_item = session['query_item']
        query_filed = session['query_filed']
        search_form.search_input.data = query_filed
        search_form.select_item.data = query_item
    elif query_item is not None:
        session['query_item'] = query_item
        session['query_filed'] = query_filed
        search_form.search_input.data = query_filed
        search_form.select_item.data = query_item
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

    if query_obj is not None:
        filter_item = query_obj.like("%"+query_filed+"%")
        report_list = Report.query.filter(or_(filter_item)).order_by(
            Report.log_id.desc()).all()
        find_count = Report.query.filter(or_(filter_item)).order_by(
            Report.log_id.desc()).count()
        # print('query_obj:%s query_filed:%s find%s'%(query_obj,query_filed,report_list))
    else:
        report_list = Report.query.order_by(Report.log_id.desc()).all()
        find_count = Report.query.order_by(Report.log_id.desc()).count()
        # print('query_obj:%s query_filed:%s find%s'%(query_obj,query_filed,report_list))

    categary = request.args.get('categary', 'case_day', type=str)
    # report_list = Report.query.order_by(Report.log_id).all()
    if categary == 'ins_cov':
        ec2_source_url = 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html'
        ec2_sock = urllib2.urlopen(ec2_source_url)
        ec2_data = ec2_sock.read()
        ec2_sock.close()
        ec2_soup = BeautifulSoup(ec2_data)
        ec2_instances = ec2_soup.findAll('code', {'class': 'code'})
        ec2_instances_tmp_list = map(lambda x: x.text, ec2_instances)
        ec2_instances_list = []
        for i in ec2_instances_tmp_list:
            if ec2_instances_list.count(i) == 0:
                ec2_instances_list.append(i)
        ec2_chart = LineChart("instance_coverage", options={
            'title': 'Instance Types Coverage Status', "height": 500})
        instance_coverdict = {}
        for report in report_list:
            if instance_coverdict.has_key(report.instance_type):
                instance_coverdict[report.instance_type] += 1
            else:
                instance_coverdict[report.instance_type] = 1
        chart_data = []
        for instance in ec2_instances_list:
            if instance_coverdict.has_key(instance):
                chart_data.append([instance, instance_coverdict[instance]])
            else:
                chart_data.append([instance, 0])
        for instance in instance_coverdict.keys():
            if ec2_instances_list.count(instance) == 0:
                chart_data.append([instance, instance_coverdict[instance]])
        sorted_chart_data = sorted(
            chart_data, key=lambda instance_type: instance_type[0])
        if len(sorted_chart_data) == 0:
            flash("No result found!")
        ec2_chart.add_column("string", "Instance Types")
        ec2_chart.add_column("number", "Test Times")
        ec2_chart.add_rows(sorted_chart_data)
        charts.register(ec2_chart)

    if categary == 'case_pass':
        ec2_case_rate = LineChart("caserate", options={
            'title': 'Case Pass Rate Report', "height": 500})
        case_data = []
        for report in report_list:
            case_data.append([report.test_date, report.pass_rate])
        sorted_case_data = sorted(
            case_data, key=lambda test_date: test_date[0])
        if len(sorted_case_data) == 0:
            flash("No result found!")
        ec2_case_rate.add_column("string", "Test Date")
        ec2_case_rate.add_column("number", "Pass Rate")
        ec2_case_rate.add_rows(sorted_case_data)
        charts.register(ec2_case_rate)

    if categary == 'case_run':
        ec2_cases_chart = LineChart("caseschart", options={
            'title': 'Cases Count', "height": 500})
        cases_total_data = []
        cases_data = []
        for report in report_list:
            cases_data.append([report.test_date, report.cases_total, report.cases_pass,
                               report.cases_fail, report.cases_other, report.cases_cancel])
        sorted_cases_data = sorted(
            cases_data, key=lambda test_date: test_date[0])
        if len(sorted_cases_data) == 0:
            flash("No result found!")
        ec2_cases_chart.add_column("string", "Test Date")
        ec2_cases_chart.add_column("number", "Total")
        ec2_cases_chart.add_column("number", "Pass")
        ec2_cases_chart.add_column("number", "Fail")
        ec2_cases_chart.add_column("number", "Other")
        ec2_cases_chart.add_column("number", "Skip/Cancel")
        ec2_cases_chart.add_rows(sorted_cases_data)
        charts.register(ec2_cases_chart)

    if categary == 'case_day':

        ec2_cases_day = LineChart("casesperday", options={
            'title': 'Cases Run Per Day', "height": 500})
        cases_per_day = []
        for report in report_list:
            is_new = True
            # cases_data.append([report.test_date, report.cases_total,report.cases_pass,report.cases_fail,report.cases_other,report.cases_cancel])
            for case in cases_per_day:
                if case[0] == report.test_date:
                    case[1] += report.cases_total
                    case[2] += report.cases_pass
                    case[3] += report.cases_fail
                    case[4] += report.cases_other
                    case[5] += report.cases_cancel
                    is_new = False
                    break
            if is_new:
                cases_per_day.append([report.test_date, report.cases_total, report.cases_pass,
                                      report.cases_fail, report.cases_other, report.cases_cancel])
        sorted_cases_per_day = sorted(
            cases_per_day, key=lambda test_date: test_date[0])
        days_list = []
        if len(sorted_cases_per_day) == 0:
            flash("No result found!")
        else:
            start_date = datetime.strptime(
                sorted_cases_per_day[0][0], '%Y-%m-%d').date()
            end_date = date.today()
            # print(end_date)
            for dt in daterange(start_date, end_date):
                day = dt.strftime("%Y-%m-%d")
                is_new = True
                for item in sorted_cases_per_day:
                    if item[0] == day:
                        days_list.append(item)
                        is_new = False
                        break
                if is_new:
                    days_list.append([dt.strftime("%Y-%m-%d"), 0, 0, 0, 0, 0])

        ec2_cases_day.add_column("string", "Test Date")
        ec2_cases_day.add_column("number", "Total")
        ec2_cases_day.add_column("number", "Pass")
        ec2_cases_day.add_column("number", "Fail")
        ec2_cases_day.add_column("number", "Other")
        ec2_cases_day.add_column("number", "Skip/Cancel")
        ec2_cases_day.add_rows(days_list)
        charts.register(ec2_cases_day)

    # if request.method == 'GET':
    #    return redirect(url_for('show_chart',categary=categary,select_item=query_item, search_input=query_filed))
    msg += 'Found %s items!' % find_count

    if search_form.validate_on_submit():

        return redirect(url_for('main.show_chart', query_item=query_item, query_filed=query_filed, categary=categary))
    flash(msg, 'info')
    return render_template('show_chart.html', categary=categary, select_item=query_item, search_input=query_filed, form=search_form)
    # return redirect(url_for('show_chart',categary=categary,select_item=query_item, search_input=query_filed))

    # ec2_chart=ColumnChart("instance_coverage", options={
    #                        'title': 'Instance Types Coverage Status'}, data_url=url_for('show_chart'))

