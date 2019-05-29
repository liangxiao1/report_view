# /usr/bin/env python
import os
import json
import sys
import re
import argparse
import logging
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

parser = argparse.ArgumentParser(description="Write results to local db")
parser.add_argument('--dir', dest='log_dir', action='store',
                    help="specify log directory", default=None, required=True)
parser.add_argument("--ami-id", dest='ami_id', action='store',
                    help="specify ami id", default=None, required=True)
parser.add_argument("--compose-id", dest='compose_id', action='store',
                    help="specify compose id if have", default=None, required=False)
parser.add_argument("--instance_available_date", dest='instance_available_date', action='store',
                    help="specify it if it is new", default=None, required=False)
parser.add_argument("--pkg_ver", dest='pkg_ver', action='store',
                    help="specify pkg version, like kernel or others", default=None, required=True)
parser.add_argument("--bug-id", dest='bug_id', action='store',
                    help="specify bug id if have", default=None, required=False)
parser.add_argument("--report_url", dest='report_url', action='store',
                    help="specify log url", default=None, required=True)
parser.add_argument("--branch_name", dest='branch_name', action='store',
                    help="specify branch name, like RHEL6|7|8", default=None, required=True)
parser.add_argument("--comments", dest='comments', action='store',
                    help="more information if have", default=None, required=False)
args = parser.parse_args()


db_engine = create_engine('sqlite:///report_data.db', echo=True)
db_session = sessionmaker(bind=db_engine)
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


def report_writer():
    instances_sub_report = {}
    log_json = args.log_dir+"/results.json"
    with open(log_json, 'r') as fh:
        report_dict = json.load(fh)
        # print(report_dict)
        print(report_dict['debuglog'])
        test_date = re.findall(
            '[0-9]{4}-[0-9]{2}-[0-9]{2}', report_dict['debuglog'])
        for x in report_dict['tests']:
            instance_type = re.findall('Cloud-.*-', x['id'])[0].split('-')[1]
            if not instances_sub_report.has_key(instance_type):
                instances_sub_report[instance_type] = {
                    'cases_other': 0, 'cases_pass': 0, 'cases_fail': 0, 'cases_cancel': 0, 'cases_total': 0, 'test_date': test_date, 'pass_rate': 0}
            instances_sub_report[instance_type]['cases_total'] += 1
            if 'PASS' in x['status']:
                instances_sub_report[instance_type]['cases_pass'] += 1
            elif 'FAIL' in x['status']:
                instances_sub_report[instance_type]['cases_fail'] += 1
            elif "CANCEL" in x['status'] or "SKIP" in x['status']:
                instances_sub_report[instance_type]['cases_cancel'] += 1
            else:
                instances_sub_report[instance_type]['cases_other'] += 1
            pass_rate = instances_sub_report[instance_type]['cases_pass']*100 / \
                (instances_sub_report[instance_type]['cases_total'] -
                 instances_sub_report[instance_type]['cases_cancel'])
            instances_sub_report[instance_type]['pass_rate'] = pass_rate

    for instance_type in instances_sub_report.keys():
        print(instance_type, instances_sub_report[instance_type])
        report = Report()
        report.ami_id = args.ami_id
        report.instance_type = instance_type
        report.compose_id = args.compose_id
        report.instance_available_date = args.instance_available_date
        report.pkg_ver = args.pkg_ver
        report.bug_id = args.bug_id
        report.report_url = args.report_url
        report.branch_name = args.branch_name
        report.comments = args.comments
        report.cases_pass = instances_sub_report[instance_type]['cases_pass']
        report.cases_fail = instances_sub_report[instance_type]['cases_fail']
        report.cases_cancel = instances_sub_report[instance_type]['cases_cancel']
        report.cases_other = instances_sub_report[instance_type]['cases_other']
        report.cases_total = instances_sub_report[instance_type]['cases_total']
        report.pass_rate = instances_sub_report[instance_type]['pass_rate']
        report.test_date = instances_sub_report[instance_type]['test_date'][0]
        session = db_session()
        session.add(report)
        session.commit()


if __name__ == "__main__":
    report_writer()
