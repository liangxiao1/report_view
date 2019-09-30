#!/usr/bin/env python

'''
This tool is for dumping image information from image task json file, 
checking whether they are released properly and update db.

'''

import json
import string
import os
import re
import sys
if sys.version.startswith('2.7'):
    print('Only support run in python3')
    sys.exit(1)
import urllib.request as request
import logging
import argparse
import boto3
import tempfile

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def update_ami(ami_id,push_task,check_result):
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
    ami_item = ProjectTab()
    session = db_session()
    ami_item= session.query(ProjectTab).filter( ProjectTab.field_3 == ami_id ).all()[0]
    session.close()
    if args.qe_state is not None:
        ami_item.field_11 = args.qe_state
        ami_item.field_12 = args.test_date
    if args.comments is not None:
        ami_item.field_13 = args.comments
    ami_item.field_14 = 'Yes'
    ami_item.field_15 = push_task
    ami_item.field_16 = check_result
    ami_item.field_17 = 'xiliang'
    session = db_session()
    session.add(ami_item)
    session.commit()

parser = argparse.ArgumentParser(
    'Dump image information and generate yamls for dva run!')
parser.add_argument('--image_url', dest='image_url', action='store',
                    help='image build task json download url', required=True)
parser.add_argument('--db_file', dest='db_file', action='store',
                    help='Optional write result to db', required=True)
parser.add_argument('--qe_state', dest='qe_state', action='store',
                    help='add test qe_state', required=False)
parser.add_argument('--comments', dest='comments', action='store',
                    help='add comments', required=False)
parser.add_argument('-d', dest='is_debug', action='store_true', default=False,
                    help='Run in debug mode', required=False)
args = parser.parse_args()
log = logging.getLogger(__name__)
if args.is_debug:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
url = args.image_url
s = request.urlopen(url)
push_task = re.findall('(\d.*\d)',url)[0]
log.info('Get data from %s' % s.geturl())
# print(s.read().decode('utf-8'))

fh, json_file = tempfile.mkstemp(suffix='.json',dir='/tmp',prefix='ami')

with open(json_file, 'b+w') as fh:
    fh.write(s.read())
log.info('Data saved to %s' % json_file)
with open(json_file, 'r') as fh:
    image_dict = json.load(fh)
#log.info(image_dict)
for i in image_dict:
    log.info("%s %s %s" % (i['name'], i['ami'], i['region']))
    try:
        client = boto3.client('ec2',region_name=i['region'])
        s=client.describe_instances()
        response = client.describe_images(
                ImageIds=[
                    i['ami'],
                ],
                DryRun=False
            )
        
        if 'Hourly' in i['name']:
            is_pub = response['Images'][0]['Public']
            if is_pub:
                log.info('Public is %s' % is_pub)
                update_ami(i['ami'],push_task,'pass')
            else:
                log.error("Public is %s" % is_pub)
                update_ami(i['ami'],push_task,'fail')
        else:
            is_pub = response['Images'][0]['Public']
            if not is_pub:
                log.info('Public is %s' % is_pub)
                update_ami(i['ami'],push_task,'pass')
            else:
                log.error("Public is %s" % is_pub)
                update_ami(i['ami'],push_task,'fail')
    except Exception as err:
        log.info(err)
        continue
os.unlink(json_file)
