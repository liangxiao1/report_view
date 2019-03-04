#!/usr/bin/env python
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

db_engine = create_engine('sqlite:///report_data.db', echo=True)

Base = declarative_base()


class Report(Base):
    __tablename__ = 'report_info'
    log_id = Column(Integer, primary_key=True)
    ami_id = Column(String)
    instance_type = Column(String)
    instance_available_date = Column(String)
    compose_id = Column(String)
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


class User(Base):
    __tablename__ = 'user_info'

    userid = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    sqlite_autoincrement = True


Base.metadata.create_all(db_engine)
'''
conn = sqlite3.connect('report_data.db')
print("Opened database successfully")

conn.execute('CREATE TABLE report_info (log_id INTEGER PRIMARY KEY,ami_id TEXT, instance_type TEXT, \
compose_id TEXT, pkg_ver TEXT,bug_id TEXT, report_url TEXT, branch_name TEXT, cases_pass INTEGER, \
cases_fail INTEGER, cases_other INTEGER, cases_total INTEGER, pass_rate INTEGER, \
test_date TEXT)')
print("Table created successfully")
conn.close()
'''
'''
Table report_info includes following fields:
    log_id: identical id of log,automatically increase,
    ami_id: ec2 ami id,
    instance_type: instance type tested,
    instance_available_date: for recording how many new instances tested in period
    compose_id: comose id if have,
    pkg_ver: kernel/other pkgs version,
    bug_id: bugzilla id if have,
    report_url: report location,
    branch_name: RHEL7/RHEL8/RHEL6,
    cases_pass: pass count,
    cases_fail: fail count,
    cases_cancel: cancel or skip cases,
    cases_other: SKIP/CANCEL count,
    cases_total: all case count,
    pass_rate: pass tatio,
    test_date: excution date
    comments: more information
'''
