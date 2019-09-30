from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_,and_
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from forms import LoginForm, SearchForm,SearchForm_v2,UpdateItemForm,NewProjectForm,EditProjectForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2

from .db_class import ProjectMap,ProjectTab
from . import libs
@main.route('/index', methods=['GET', 'POST'])
def index():
    projects= ProjectMap.query.all()
    return render_template('index.html',projects=projects)


@main.route('/view', methods=['GET', 'POST'])
def view():
    print("reueqt %s" % request.args)
    projects= ProjectMap.query.all()
    project_name = request.args.get('project_name')
    if project_name == None:
        flash('Please select project name!')
        return redirect(url_for('main.index'))
    per_page_default = 50
    search_form = SearchForm_v2(csrf_enabled=True)
    print('xiliang per_page default %s'%per_page_default)
    per_page = request.args.get('per_page')
    if per_page is None and not session.has_key('per_page'):
        per_page = per_page_default
        session['per_page'] = per_page
    elif per_page is None and session.has_key('per_page'):
        per_page = session['per_page']
    elif per_page is not None:
        session['per_page'] = per_page

    drop_list=libs.init_droplist(project_name)

    msg = ''
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        flash('No project named %s' % project_name,'error')
        return redirect(url_for('main.index'))
    #ProjectTab.__table__.create(report_db.get_engine())
    project_data = ProjectTab.query.filter_by(project_name=project_name).all()
    if len(project_data) == 0 or project_data == None:
        flash('No data found %s' % project_name,'error')
    project_items=libs.init_project_titles(project_name)

    search_form.set_choices(drop_list)
    #pagination = libs.search_db(search_form=search_form,project_name=project_name,submit=search_form.validate_on_submit(),reset=search_form.reset.data)
    find_count = 0
    page = request.args.get('page', 1, type=int)
    query_obj = None
    if search_form.validate_on_submit():
        print('item select %s, search input %s'% (search_form.select_item.data,search_form.search_input.data))
        if search_form.reset.data:
            msg += "Clear all filters!"
            flash(msg,'info')
            # session.clear()
            session.pop('search_input', None)
            session.pop('select_item', None)
            query_obj = None
            search_form.select_item.data = None
            return redirect(url_for('main.view',project_name=project_name))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data 
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    
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
    items_list = libs.init_project_titles(project_name)
    data_list = [ProjectTab.project_id,ProjectTab.project_name,ProjectTab.field_1,\
            ProjectTab.field_2,ProjectTab.field_3,ProjectTab.field_4,ProjectTab.field_5,\
        ProjectTab.field_6,ProjectTab.field_7,ProjectTab.field_8,ProjectTab.field_9,ProjectTab.field_10,\
        ProjectTab.field_11,ProjectTab.field_12,ProjectTab.field_13,ProjectTab.field_14,ProjectTab.field_15,\
        ProjectTab.field_16,ProjectTab.field_17,ProjectTab.field_18,ProjectTab.field_19,ProjectTab.field_20]
    for item in zip(items_list,data_list):
            if select_item is not None and select_item in item[0]:
                    print("quey_obj found%s"%item[1])
                    query_obj=item[1]
                    break
    
    if query_obj is not None:
        filter_item = query_obj.like("%"+search_input+"%")
        pagination = ProjectTab.query.filter(and_(filter_item,ProjectTab.project_name==project_name)).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=int(per_page), error_out=False)
        #project_data = ProjectTab.query.filter(and_(filter_item,ProjectTab.project_name==project_name)).order_by(
        #    ProjectTab.id.desc()).all()
    else:
        pagination = ProjectTab.query.filter_by(project_name=project_name).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=int(per_page), error_out=False)
        print(pagination.items)

    find_count = pagination.total
    
    projects_data = []
    for i in pagination.items:
        projects_data.append([i.id,i.project_name,i.field_1,\
            i.field_2,i.field_3,i.field_4,i.field_5,\
        i.field_6,i.field_7,i.field_8,i.field_9,i.field_10,\
        i.field_11,i.field_12,i.field_13,i.field_14,i.field_15,\
        i.field_16,i.field_17,i.field_18,i.field_19,i.field_20])

    page = request.args.get('page', 1, type=int)
    msg += 'Found %s items in %s pages!' % (find_count,pagination.pages)
    
    if search_form.validate_on_submit():
        flash(msg, category='info')
        return redirect(url_for('main.view', select_item=select_item, search_input=search_input, project_name=project_name,per_page=per_page))
    return render_template('view.html', per_page=session['per_page'], form=search_form, project_items=project_items, project_data=projects_data, pagination=pagination, select_item=select_item, search_input=search_input,project_name=project_name,projects=projects)