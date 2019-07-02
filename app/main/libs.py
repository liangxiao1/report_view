from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from forms import LoginForm, SearchForm,SearchForm_v2,UpdateItemForm,NewProjectForm,EditProjectForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2

from .db_class import ProjectMap,ProjectTab
import logging

log=logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def init_droplist(project_name):
    '''
    Return a list for searchform drop list set
    '''
    drop_list = []
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        log.error('No project named %s' % project_name)
    print("type is %s"%len(project[0].field_7))
    if project[0].field_1 is not '' and  len(project[0].field_1) > 0: 
        drop_list.append((project[0].field_1,project[0].field_1))
    if project[0].field_2 is not '' and  len(project[0].field_2) > 0:
        drop_list.append((project[0].field_2,project[0].field_2))
    if project[0].field_3 is not '' and  len(project[0].field_3) > 0:
        drop_list.append((project[0].field_3,project[0].field_3))
    if project[0].field_4 is not '' and  len(project[0].field_4) > 0:
        drop_list.append((project[0].field_4,project[0].field_4))
    if project[0].field_5 is not '' and  len(project[0].field_5) > 0:
        drop_list.append((project[0].field_5,project[0].field_5))
    if project[0].field_6 is not '' and  len(project[0].field_6) > 0:
        drop_list.append((project[0].field_6,project[0].field_6))
    if project[0].field_7 is not '' and  len(project[0].field_7) > 0:
        drop_list.append((project[0].field_7,project[0].field_7))
    if project[0].field_8 is not '' and  len(project[0].field_8) > 0:
        drop_list.append((project[0].field_8,project[0].field_8))
    if project[0].field_9 is not '' and  len(project[0].field_9) > 0:
        drop_list.append((project[0].field_9,project[0].field_9))
    if project[0].field_10 is not '' and  len(project[0].field_10) > 0:
        drop_list.append((project[0].field_10,project[0].field_10))
    if project[0].field_11 is not '' and  len(project[0].field_11) > 0:
        drop_list.append((project[0].field_11,project[0].field_11))
    if project[0].field_12 is not '' and  len(project[0].field_12) > 0:
        drop_list.append((project[0].field_12,project[0].field_12))
    if project[0].field_13 is not '' and  len(project[0].field_13) > 0:
        drop_list.append((project[0].field_13,project[0].field_13))
    if project[0].field_14 is not '' and  len(project[0].field_14) > 0:
        drop_list.append((project[0].field_14,project[0].field_14))
    if project[0].field_15 is not '' and  len(project[0].field_15) > 0:
        drop_list.append((project[0].field_15,project[0].field_15))
    if project[0].field_16 is not '' and  len(project[0].field_16) > 0:
        drop_list.append((project[0].field_16,project[0].field_16))
    if project[0].field_17 is not '' and  len(project[0].field_17) > 0:
        drop_list.append((project[0].field_17,project[0].field_17))
    if project[0].field_18 is not '' and  len(project[0].field_18) > 0:
        drop_list.append((project[0].field_18,project[0].field_18))
    if project[0].field_19 is not '' and  len(project[0].field_19) > 0:
        drop_list.append((project[0].field_19,project[0].field_19))
    if project[0].field_20 is not '' and  len(project[0].field_20) > 0:
        drop_list.append((project[0].field_20,project[0].field_20))
    return drop_list

def init_project_titles(project_name):
    '''
    Return a project tile map list
    '''
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        log.error('No project named %s' % project_name)
    project_data = ProjectTab.query.filter_by(project_name=project_name).all()
    if len(project_data) == 0 or project_data == None:
        flash('No data found %s' % project_name,'error')
    project_items=[]
    project_items.append("id")
    project_items.append("project_name")
    print("type is %s"%len(project[0].field_7))
    if project[0].field_1 is not '' and  len(project[0].field_1) > 0: 
        project_items.append(project[0].field_1)
    if project[0].field_2 is not '' and  len(project[0].field_2) > 0:
        project_items.append(project[0].field_2)
    if project[0].field_3 is not '' and  len(project[0].field_3) > 0:
        project_items.append(project[0].field_3)
    if project[0].field_4 is not '' and  len(project[0].field_4) > 0:
        project_items.append(project[0].field_4)
    if project[0].field_5 is not '' and  len(project[0].field_5) > 0:
        project_items.append(project[0].field_5)
    if project[0].field_6 is not '' and  len(project[0].field_6) > 0:
        project_items.append(project[0].field_6)
    if project[0].field_7 is not '' and  len(project[0].field_7) > 0:
        project_items.append(project[0].field_7)
    if project[0].field_8 is not '' and  len(project[0].field_8) > 0:
        project_items.append(project[0].field_8)
    if project[0].field_9 is not '' and  len(project[0].field_9) > 0:
        project_items.append(project[0].field_9)
    if project[0].field_10 is not '' and  len(project[0].field_10) > 0:
        project_items.append(project[0].field_10)
    if project[0].field_11 is not '' and  len(project[0].field_11) > 0:
        project_items.append(project[0].field_11)
    if project[0].field_12 is not '' and  len(project[0].field_12) > 0:
        project_items.append(project[0].field_12)
    if project[0].field_13 is not '' and  len(project[0].field_13) > 0:
        project_items.append(project[0].field_13)
    if project[0].field_14 is not '' and  len(project[0].field_14) > 0:
        project_items.append(project[0].field_14)
    if project[0].field_15 is not '' and  len(project[0].field_15) > 0:
        project_items.append(project[0].field_15)
    if project[0].field_16 is not '' and  len(project[0].field_16) > 0:
        project_items.append(project[0].field_16)
    if project[0].field_17 is not '' and  len(project[0].field_17) > 0:
        project_items.append(project[0].field_17)
    if project[0].field_18 is not '' and  len(project[0].field_18) > 0:
        project_items.append(project[0].field_18)
    if project[0].field_19 is not '' and  len(project[0].field_19) > 0:
        project_items.append(project[0].field_19)
    if project[0].field_20 is not '' and  len(project[0].field_20) > 0:
        project_items.append(project[0].field_20)
    return project_items

def search_db(search_form=None,project_name=None,submit=None,reset=None):
    msg=''
    query_obj = None
    per_page_default = 100
    find_count = 0
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)
    if submit:
        print('item select %s, search input %s'% (search_form.select_item.data,search_form.search_input.data))
        if reset:
            msg += "Clear all filters!"
            flash(msg,'info')
            # session.clear()
            session.pop('search_input', None)
            session.pop('select_item', None)
            query_obj = None
            search_form.select_item.data = None
            return redirect(url_for('main.home'))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data 
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    
    find_count = ProjectTab.query.count()
    if select_item is None and session.has_key("select_item"):
        select_item = session['select_item']
        search_input = session['search_input']
        search_form.search_input.data = search_input
        search_form.select_item.data = select_item
    elif select_item is not None:
        session['select_item'] = select_item
        session['search_input'] = search_input
        search_form.search_input.data = search_input
        search_form.select_item.data = select_item
    items_dict = {}
    items_list = init_project_titles(project_name)
    data_list = [ProjectTab.project_id,ProjectTab.project_name,ProjectTab.field_1,\
            ProjectTab.field_2,ProjectTab.field_3,ProjectTab.field_4,ProjectTab.field_5,ProjectTab.field_1,\
        ProjectTab.field_6,ProjectTab.field_7,ProjectTab.field_8,ProjectTab.field_9,ProjectTab.field_10,\
        ProjectTab.field_11,ProjectTab.field_12,ProjectTab.field_13,ProjectTab.field_14,ProjectTab.field_15,\
        ProjectTab.field_16,ProjectTab.field_17,ProjectTab.field_18,ProjectTab.field_19,ProjectTab.field_20]
    print(items_list)
    for item in zip(items_list,data_list):
            if select_item is not None and select_item in item[0]:
                    print("query_obj found%s"%item[1])
                    query_obj=item[1]
                    break
    
    if query_obj is not None:
        filter_item = query_obj.like("%"+search_input+"%")
        print(' filter_item %s'%filter_item)
        pagination = ProjectTab.query.filter(or_(filter_item)).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
        find_count = ProjectTab.query.filter(or_(filter_item)).count()
    else:
        find_count = ProjectTab.query.filter_by(project_name=project_name).count()
        pagination = ProjectTab.query.filter_by(project_name=project_name).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=session['per_page'], error_out=False)

    reports = pagination.items
    msg += 'Found %s items!' % find_count
    flash(msg, category='info')
    return pagination
    if submit:
        print('xiliang3')
        return redirect(url_for('main.view', select_item=select_item, search_input=search_input, project_name=project_name, pagination=pagination))
    return render_template('view.html', per_page=session['per_page'], form=search_form, reports=reports, pagination=pagination, select_item=select_item, search_input=search_input,project_name=project_name)

    

