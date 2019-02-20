#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, session, url_for
from flask_bootstrap import Bootstrap
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import Pagination
from flask_sqlalchemy import BaseQuery
import time
from sqlalchemy import or_


import google
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///report_data.db'

bootstrap = Bootstrap(app)
app.secret_key = 'development key'

report_db = SQLAlchemy(app)


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
        #print("%s-%s-%s" % (query_filed, query_item, session['query_item']))

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    year_1 = time.strftime("%Y")
    year_2 = int(time.strftime("%Y"))-1
    year_3 = int(time.strftime("%Y"))-3
    year_4 = int(time.strftime("%Y"))-4

    filter_1y = Report.test_date.like(year_1+"%")
    filter_2y = Report.test_date.like(str(year_2)+"%")
    filter_3y = Report.test_date.like(str(year_3)+"%")
    years = request.args.get('years', 1, type=int)
    if years == 1:
        filter = or_(filter_1y)
    elif years == 2:
        filter = or_(filter_1y, filter_2y)
    elif years == 3:
        filter = or_(filter_1y, filter_2y, filter_3y)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
    # app.run(debug = True)
