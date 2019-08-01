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
from bs4 import BeautifulSoup as BS
#import request
import sys

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

parser = argparse.ArgumentParser(description="Write images information to to local db")
parser.add_argument('--task_url', dest='task_url', action='store',
                    help='task_url for build amis', required=True)
parser.add_argument('--rcm', dest='rcm', action='store',
                    help='rcm ticket id', required=True)
parser.add_argument('--log_url', dest='log_url', action='store',
                    help='dva test result log url, it is optional can be edited after test done', required=False)
parser.add_argument('--qe_state', dest='qe_state', action='store',
                    help='pass/fail/abondon, qe ack or not, it is optional and can be edited at last', required=False)
parser.add_argument('--test_date', dest='test_date', action='store',
                    help='qe test date, it is optional and can be edited at last', required=False)
parser.add_argument('--db_file', dest='db_file', action='store',
                    help='db file path', required=True)
parser.add_argument('-d', dest='is_debug', action='store_true', default=False,
                    help='Run in debug mode', required=False)
args = parser.parse_args()
log = logging.getLogger(__name__)
if args.is_debug:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

if not os.path.exists(args.db_file):
    log.error("Cannot find %s" % args.db_file)
    sys.exit(1)
db_engine = create_engine('sqlite:///%s'%args.db_file, echo=True)
db_session = sessionmaker(bind=db_engine)
Base = declarative_base()

class ProjectTab(Base):
    __tablename__ = 'project_data'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    project_name = Column(String)
    field_1 = Column(String)
    field_2 = Column(String)
    field_3 = Column(String)
    field_4 = Column(String)
    field_5 = Column(String)
    field_6 = Column(String)
    field_7 = Column(String)
    field_8 = Column(String)
    field_9 = Column(String)
    field_10 = Column(String)
    field_11 = Column(String)
    field_12 = Column(String)
    field_13 = Column(String)
    field_14 = Column(String)
    field_15 = Column(String)
    field_16 = Column(String)
    field_17 = Column(String)
    field_18 = Column(String)
    field_19 = Column(String)
    field_20 = Column(String)
    sqlite_autoincrement = True



def report_writer():
    taskurl=args.task_url
    jsonurl="%s/log/images.json?format=raw" % taskurl
    task_fh = urlopen(taskurl)
    soup = BS(task_fh.read(),'lxml')
    #elems = soup.findAll('a', {'title': 'title here'})
    #log.info(soup)
    tds = soup.findAll(['dd','dt','br'])
    log.info(tds)

    for td in tds:
        inner_text = td.text
        if 'ID' in inner_text:
            task_id=tds[tds.index(td)+1].text
        if 'Created' in inner_text:
            create_date=tds[tds.index(td)+1].text
        if 'target' in inner_text:
            target=inner_text.split(':')[-1].replace('"','')
        log.info(inner_text)
    #log.info(elems[0].text)
    log.info("task_id: %s" % task_id)
    log.info("created date: %s" % create_date)
    log.info("target is: %s" % target)
    s = urlopen(jsonurl)
    log.info('Get data from %s' % s.geturl())
    # print(s.read().decode('utf-8'))
    json_file = '/tmp/images.json'
    if os.path.exists(json_file):
        os.unlink(json_file)
        log.debug('Removed exists %s' % json_file)
    with open(json_file, 'b+w') as fh:
        fh.write(s.read())
    log.info('Data saved to %s' % json_file)
    with open(json_file,'r') as fh:
        img_dict=json.load(fh)
    for i in img_dict:
        log.info(i)
        ami_item = ProjectTab()
        ami_item.project_name = 'image_validate_aws'
        ami_item.field_1 = args.rcm
        ami_item.field_2 = task_id
        ami_item.field_3 = i['ami']
        ami_item.field_4 = i['name']
        ami_item.field_5 = i['region']
        ami_item.field_6 = i['ena_support']
        ami_item.field_7 = i["release"]['respin']
        ami_item.field_8 = target
        ami_item.field_9 = create_date
        ami_item.field_10 = args.log_url
        ami_item.field_11 = args.qe_state
        ami_item.field_12 = args.test_date
        ami_item.field_13 = ''
        ami_item.field_14 = ''
        ami_item.field_15 = ''
        ami_item.field_16 = ''
        ami_item.field_17 = 'xiliang'
        session = db_session()
        session.add(ami_item)
        session.commit()

if __name__ == "__main__":
    report_writer()
