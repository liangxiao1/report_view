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
import pdb
import pandas as pd

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen

parser = argparse.ArgumentParser(description="Parse lcov html report")
parser.add_argument('--report_dir', dest='report_dir', action='store',
                    help='lcov html report dir', required=True)
parser.add_argument('--report_url', dest='report_url', action='store',
                    help='url for web access', required=True)
parser.add_argument('--is_write', dest='is_write', action='store_true',
                    help='write data to db', required=False)
parser.add_argument('--kernel_version', dest='kernel_version', action='store',
                    help='kernel version', required=True)
parser.add_argument('--owner', dest='owner', action='store',
                    help='owner for test', required=True)
parser.add_argument('--test_suite', dest='test_suite', action='store',
                    help='test suite name', required=True)
parser.add_argument('--branch_name', dest='branch_name', action='store',
                    help='branch name, eg. RHEL7.0/RHEL8.0/RHEL6.10', required=True)
parser.add_argument('--comment', dest='comment', action='store',
                    help='comments if have', required=False)
parser.add_argument('-d', dest='is_debug', action='store_true', default=False,
                    help='Run in debug mode', required=False)
parser.add_argument('--db_file', dest='db_file', action='store',
                    help='db file path', required=True)

args = parser.parse_args()
log = logging.getLogger(__name__)
if args.is_debug:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s:%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

if args.is_write and not os.path.exists(args.db_file):
    log.error("Cannot find %s" % args.db_file)
    sys.exit(1)

top_index = '%s/index.html' % args.report_dir
if not os.path.exists(top_index):
    log.error("Cannot find %s" % top_index)
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
    fd=open(top_index)
    soup = BS(fd,'lxml')
    log.info('parsing all sub index.html')
    tds=soup.findAll('td',{"class": "coverFile"})
    subindex_list = []
    for i in tds:
        log.info('find %s' % i.a['href'] )
        subindex_list.append(i.a['href'])
    for i in subindex_list:
        sub_index = "%s/%s" % (args.report_dir, i)
        log.info('reading %s' % sub_index)
        with open(sub_index) as fh:
            soup = BS(fh,'lxml')
            tds=soup.findAll('td',["headerValue"])
            #log.info
            sub_dir = tds[0].get_text().replace('top level - ','')
            test_date = tds[2].get_text()
        #tables = BS(open(sub_index,'r').read()).find('table')
        df = pd.read_html(sub_index,match='Filename')
        log.info(df[0])
        #df = df[0].drop([1, 2], axis = 1)

        df = df[0].dropna(how='all')
        df = df[df[0] != 'Filename']
        df = df.dropna(axis=1,how='all')
        #df = df.reset_index()
        df.columns = range(df.shape[1])
        #header = df.iloc[0]
        #df = df[1:]
        #df = df.rename(columns = header)
        log.info("Filename %s Line ratio %s" % (df[0],df[3]))
        log.info(type(df[0]))
        #pdb.set_trace()
        log.info(df)
        for index, row in df.iterrows():
            if 'Filename' in row[0]:
                continue
            filename = row[0]
            line_passration = row[1].replace(u'\xa0%', '').strip(' ')
            try:
                line_cover = row[2].split('/')[0]
                line_total = row[2].split('/')[1]
            except Exception as err:
                log.info('line: %s %s %s'%(row[4],err,row))
                sys.exit(1)
            func_passration = row[3].replace(u'\xa0%', '').strip(' ')
            try:
                func_cover = row[4].split('/')[0]
                func_total = row[4].split('/')[1]
            except Exception as err:
                log.info('line: %s %s %s'%(row[4],err,row))
                sys.exit(1)
            print(filename, line_passration,line_cover,line_total,func_passration,func_cover ,func_total,test_date)
            new_item = ProjectTab()
            new_item.project_id = 2
            new_item.project_name = 'codecoverage_kernel'
            new_item.field_1 = "%s/%s" % (sub_dir,filename)
            new_item.field_2 = args.kernel_version
            new_item.field_3 = line_cover
            new_item.field_4 = line_total
            new_item.field_5 = line_passration
            new_item.field_6 = func_cover
            new_item.field_7 = func_total
            new_item.field_8 = func_passration
            new_item.field_9 = args.report_url
            new_item.field_10 = args.branch_name
            new_item.field_11 = args.test_suite
            new_item.field_12 = args.owner
            new_item.field_13 = test_date
            if args.comment is not None:
                new_item.field_14 = args.comment
            else:
                new_item.field_14 = ''
            session = db_session()
            session.add(new_item)
            session.commit()

    sys.exit(0)

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
