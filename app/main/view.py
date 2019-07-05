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
    projects= ProjectMap.query.all()
    project_name = request.args.get('project_name')
    if project_name == None:
        flash('Please select project name!')
        return redirect(url_for('main.index'))
    per_page_default = 50
    search_form = SearchForm_v2(csrf_enabled=True)
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
        print("xiliang----")
    project_items=libs.init_project_titles(project_name)

    search_form.set_choices(drop_list)
    #pagination = libs.search_db(search_form=search_form,project_name=project_name,submit=search_form.validate_on_submit(),reset=search_form.reset.data)
    #reports = ProjectTab.query.all()

    per_page_default = 100
    find_count = 0
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)
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
            return redirect(url_for('main.view',project_name='test4'))
        else:
            select_item = search_form.select_item.data
            search_input = search_form.search_input.data 
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    
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
            ProjectTab.field_2,ProjectTab.field_3,ProjectTab.field_4,ProjectTab.field_5,ProjectTab.field_1,\
        ProjectTab.field_6,ProjectTab.field_7,ProjectTab.field_8,ProjectTab.field_9,ProjectTab.field_10,\
        ProjectTab.field_11,ProjectTab.field_12,ProjectTab.field_13,ProjectTab.field_14,ProjectTab.field_15,\
        ProjectTab.field_16,ProjectTab.field_17,ProjectTab.field_18,ProjectTab.field_19,ProjectTab.field_20]
    print(items_list)
    for item in zip(items_list,data_list):
            if select_item is not None and select_item in item[0]:
                    print("quey_obj found%s"%item[1])
                    query_obj=item[1]
                    break
    
    if query_obj is not None:
    #if search_form.validate_on_submit():
        filter_item = query_obj.like("%"+search_input+"%")
        #print(' filter_item %s'%filter_item)
        pagination = ProjectTab.query.filter(and_(filter_item,ProjectTab.project_name==project_name)).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
        #print(pagination.items)
        project_data = ProjectTab.query.filter(and_(filter_item,ProjectTab.project_name==project_name)).order_by(
            ProjectTab.id.desc()).all()
        #find_count = ProjectTab.query.filter(or_(filter_item)).count()
    else:
        #find_count = ProjectTab.query.filter_by(project_name=project_name).count()
        pagination = ProjectTab.query.filter_by(project_name=project_name).order_by(
            ProjectTab.id.desc()).paginate(page, per_page=session['per_page'], error_out=False)
        print(pagination.items)
        project_data = ProjectTab.query.filter(and_(ProjectTab.project_name==project_name)).order_by(
            ProjectTab.id.desc()).all()
    find_count = len(pagination.items)
    
    projects_data = []
    for i in project_data:
        projects_data.append([i.id,i.project_name,i.field_1,\
            i.field_2,i.field_3,i.field_4,i.field_5,\
        i.field_6,i.field_7,i.field_8,i.field_9,i.field_10,\
        i.field_11,i.field_12,i.field_13,i.field_14,i.field_15,\
        i.field_16,i.field_17,i.field_18,i.field_19,i.field_20])
    #print( projects_data)

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)
    msg += 'Found %s items!' % find_count
    
    if search_form.validate_on_submit():
        flash(msg, category='info')
        print('xiliang3')
        return redirect(url_for('main.view', select_item=select_item, search_input=search_input, project_name=project_name))
    return render_template('view.html', per_page=session['per_page'], form=search_form, project_items=project_items, project_data=projects_data, pagination=pagination, select_item=select_item, search_input=search_input,project_name=project_name,projects=projects)