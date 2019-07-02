from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_

from forms import LoginForm, SearchForm,SearchForm_v2, UpdateItemForm,NewProjectForm,EditProjectForm,ProjectDataForm,EditProjectDataForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2

from .db_class import ProjectMap,ProjectTab

from . import libs

@main.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    projects= ProjectMap.query.all()
    project_name = request.args.get('project_name')
    if project_name == None:
        flash('Please select project name!')
        return redirect(url_for('main.index'))
    per_page_default = 50
    search_form = SearchForm_v2(csrf_enabled=True)
    drop_list=libs.init_droplist(project_name)
    search_form.set_choices(drop_list)
    msg = ''
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        flash('No project named %s' % project_name,'error')
        return redirect(url_for('main.index'))
    #ProjectTab.__table__.create(report_db.get_engine())
    project_data_form = ProjectDataForm()
    
    project_data = ProjectTab.query.filter_by(project_name=project_name).all()
    if len(project_data) == 0 or project_data == None:
        flash('No data found in project %s' % project_name,'error')
    project_data = ProjectTab()
    project_items=libs.init_project_titles(project_name)
    
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
            return redirect(url_for('main.view',project_name=project_name, select_item=select_item,search_input=search_input))
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')
    
    project_data_form.project_id.data = project[0].project_id
    project_data_form.project_name.data = project[0].project_name
    if len(project_items) > 2:
        if len(project_items[2]) > 0: project_data_form.field_1.label.text = project_items[2]
    if len(project_items) > 3:
        if len(project_items[3]) > 0: project_data_form.field_2.label.text = project_items[3]
    if len(project_items) > 4:
        if len(project_items[4]) > 0: project_data_form.field_3.label.text = project_items[4]
    if len(project_items) > 5:
        if len(project_items[5]) > 0: project_data_form.field_4.label.text = project_items[5]
    if len(project_items) > 6:
        if len(project_items[6]) > 0: project_data_form.field_5.label.text = project_items[6]
    if len(project_items) > 7:    
        if len(project_items[7]) > 0: project_data_form.field_6.label.text = project_items[7]
    if len(project_items) > 8:
        if len(project_items[8]) > 0: project_data_form.field_7.label.text = project_items[8]
    if len(project_items) > 9:
        if len(project_items[9]) > 0: project_data_form.field_8.label.text = project_items[9]
    if len(project_items) > 10:
        if len(project_items[10]) > 0: project_data_form.field_9.label.text = project_items[10]
    if len(project_items) > 11:
        if len(project_items[11]) > 0: project_data_form.field_10.label.text = project_items[11]
    if len(project_items) > 12:
        if len(project_items[12]) > 0: project_data_form.field_11.label.text = project_items[12]
    if len(project_items) > 13:
        if len(project_items[13]) > 0: project_data_form.field_12.label.text = project_items[13]
    if len(project_items) > 14:
        if len(project_items[14]) > 0: project_data_form.field_13.label.text = project_items[14]
    if len(project_items) > 15:
        if len(project_items[15]) > 0: project_data_form.field_14.label.text = project_items[15]
    if len(project_items) > 16:
        if len(project_items[16]) > 0: project_data_form.field_15.label.text = project_items[16]
    if len(project_items) > 17:
        if len(project_items[17]) > 0: project_data_form.field_16.label.text = project_items[17]
    if len(project_items) > 18:
        if len(project_items[18]) > 0: project_data_form.field_17.label.text = project_items[18]
    if len(project_items) > 19:
        if len(project_items[19]) > 0: project_data_form.field_18.label.text = project_items[19]
    if len(project_items) > 10:
        if len(project_items[20]) > 0: project_data_form.field_19.label.text = project_items[20]
    if len(project_items) > 21:
        if len(project_items[21]) > 0: project_data_form.field_20.label.text = project_items[21]
    if len(project_items) > 22:
        if len(project_items[22]) > 0: project_data_form.field_21.label.text = project_items[22]
        
    if project_data_form.validate_on_submit():
        project_data.project_id = project_data_form.project_id.data
        project_data.project_name = project_data_form.project_name.data
        print(len(project_items), project_data_form.field_1.data)
        if len(project_items) > 2:
            if len(project_items[2]) > 0: project_data.field_1 = project_data_form.field_1.data
        if len(project_items) > 3:
            if len(project_items[3]) > 0: project_data.field_2 = project_data_form.field_2.data
        if len(project_items) > 4:
            if len(project_items[4]) > 0: project_data.field_3 = project_data_form.field_3.data
        if len(project_items) > 5:
            if len(project_items[5]) > 0: project_data.field_4 = project_data_form.field_4.data
        if len(project_items) > 6:
            if len(project_items[6]) > 0: project_data.field_5 = project_data_form.field_5.data
        if len(project_items) > 7:
            if len(project_items[7]) > 0: project_data.field_6 = project_data_form.field_6.data
        if len(project_items) > 8:
            if len(project_items[8]) > 0: project_data.field_7 = project_data_form.field_7.data
        if len(project_items) > 9:
            if len(project_items[9]) > 0: project_data.field_8 = project_data_form.field_8.data
        if len(project_items) > 10:
            if len(project_items[10]) > 0: project_data.field_9 = project_data_form.field_9.data
        if len(project_items) > 11:
            if len(project_items[11]) > 0: project_data.field_10 = project_data_form.field_10.data
        if len(project_items) > 12:
            if len(project_items[12]) > 0: project_data.field_11 = project_data_form.field_11.data
        if len(project_items) > 13:
            if len(project_items[13]) > 0: project_data.field_12 = project_data_form.field_12.data
        if len(project_items) > 14:
            if len(project_items[14]) > 0: project_data.field_13 = project_data_form.field_13.data
        if len(project_items) > 15:
            if len(project_items[15]) > 0: project_data.field_14 = project_data_form.field_14.data
        if len(project_items) > 16:
            if len(project_items[16]) > 0: project_data.field_15 = project_data_form.field_15.data
        if len(project_items) > 17:
            if len(project_items[17]) > 0: project_data.field_16 = project_data_form.field_16.data
        if len(project_items) > 18:
            if len(project_items[18]) > 0: project_data.field_17 = project_data_form.field_17.data
        if len(project_items) > 19:
            if len(project_items[19]) > 0: project_data.field_18 = project_data_form.field_18.data
        if len(project_items) > 20:
            if len(project_items[20]) > 0: project_data.field_19 = project_data_form.field_19.data
        if len(project_items) > 21:
            if len(project_items[21]) > 0: project_data.field_20 = project_data_form.field_20.data
        if len(project_items) > 22:
            if len(project_items[22]) > 0: project_data.field_21 = project_data_form.field_21.data
        report_db.session.add(project_data)
        report_db.session.commit()
        flash("Added successfully!",'info')
        return redirect(url_for('main.view',project_name=project_name))
    
    reports = ProjectTab.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)

    clear_session = request.args.get('clear', 0, type=int)
    find_count = 0
    find_count = ProjectTab.query.count()

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    
    return render_template('add_data.html', form=search_form,project_name=project_name,project_items=project_items, project_data=project_data,  select_item=select_item, search_input=search_input,project_data_form=project_data_form,projects=projects)

@main.route('/update_data', methods=['GET', 'POST'])
@login_required
def update_data():
    projects= ProjectMap.query.all()
    per_page_default=50
    log_id = request.args.get('log_id')
    if log_id == None:
        flash('Please specify log_id for edit!')
        return redirect(url_for('main.home'))
    project_datas = ProjectTab.query.filter_by(id=log_id).all()
    if len(project_datas) == 0 or project_datas == None:
        flash('No data found which id is %s' % log_id,'error')
        return redirect(url_for('main.home'))
    project_name = project_datas[0].project_name

    search_form = SearchForm_v2(csrf_enabled=True)
    drop_list=libs.init_droplist(project_name)
    search_form.set_choices(drop_list)
    msg = ''
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        flash('No project named %s' % project_name,'error')
        return redirect(url_for('main.home'))
    #ProjectTab.__table__.create(report_db.get_engine())
    project_data_form = EditProjectDataForm()
    

    project_items=libs.init_project_titles(project_name)
    
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
            return redirect(url_for('main.view',project_name=project_name, select_item=select_item,search_input=search_input))
    else:
        select_item = request.args.get('select_item')
        search_input = request.args.get('search_input')

    project_data_form.id.data = project_datas[0].id
    project_data_form.project_name.data = project[0].project_name
    project_data_form.project_id.data = project[0].project_id
    project_data_form.project_name.data = project[0].project_name
    
    if project_data_form.validate_on_submit():
        if project_data_form.submit.data:
            project_data = ProjectTab.query.filter_by(id=log_id).all()[0]
            project_data.id=project_data_form.id.data
            project_data.project_id = project_data_form.project_id.data
            project_data.project_name = project_data_form.project_name.data
            print(len(project_items), project_data_form.field_1.data)
            if len(project_items) > 2:
                if len(project_items[2]) > 0: project_data.field_1 = project_data_form.field_1.data
                print("project_data_form.field_2.data %s" % project_data_form.field_2.data)
            if len(project_items) > 3:
                if len(project_items[3]) > 0: project_data.field_2 = project_data_form.field_2.data
            if len(project_items) > 4:
                if len(project_items[4]) > 0: project_data.field_3 = project_data_form.field_3.data
            if len(project_items) > 5:
                if len(project_items[5]) > 0: project_data.field_4 = project_data_form.field_4.data
            if len(project_items) > 6:
                if len(project_items[6]) > 0: project_data.field_5 = project_data_form.field_5.data
            if len(project_items) > 7:
                if len(project_items[7]) > 0: project_data.field_6 = project_data_form.field_6.data
            if len(project_items) > 8:
                if len(project_items[8]) > 0: project_data.field_7 = project_data_form.field_7.data
            if len(project_items) > 9:
                if len(project_items[9]) > 0: project_data.field_8 = project_data_form.field_8.data
            if len(project_items) > 10:
                if len(project_items[10]) > 0: project_data.field_9 = project_data_form.field_9.data
            if len(project_items) > 11:
                if len(project_items[11]) > 0: project_data.field_10 = project_data_form.field_10.data
            if len(project_items) > 12:
                if len(project_items[12]) > 0: project_data.field_11 = project_data_form.field_11.data
            if len(project_items) > 13:
                if len(project_items[13]) > 0: project_data.field_12 = project_data_form.field_12.data
            if len(project_items) > 14:
                if len(project_items[14]) > 0: project_data.field_13 = project_data_form.field_13.data
            if len(project_items) > 15:
                if len(project_items[15]) > 0: project_data.field_14 = project_data_form.field_14.data
            if len(project_items) > 16:
                if len(project_items[16]) > 0: project_data.field_15 = project_data_form.field_15.data
            if len(project_items) > 17:
                if len(project_items[17]) > 0: project_data.field_16 = project_data_form.field_16.data
            if len(project_items) > 18:
                if len(project_items[18]) > 0: project_data.field_17 = project_data_form.field_17.data
            if len(project_items) > 19:
                if len(project_items[19]) > 0: project_data.field_18 = project_data_form.field_18.data
            if len(project_items) > 20:
                if len(project_items[20]) > 0: project_data.field_19 = project_data_form.field_19.data
            if len(project_items) > 21:
                if len(project_items[21]) > 0: project_data.field_20 = project_data_form.field_20.data
            if len(project_items) > 22:
                if len(project_items[22]) > 0: project_data.field_21 = project_data_form.field_21.data
            report_db.session.add(project_data)
            #report_db.session.merge(project_data)
            report_db.session.commit()
            flash("Updated successfully!",'info')
            return redirect(url_for('main.view',project_name=project_name))
    if len(project_items) > 2:
        if len(project_items[2]) > 0:
            project_data_form.field_1.label.text = project_items[2]
            project_data_form.field_1.data = project_datas[0].field_1
    if len(project_items) > 3:
        if len(project_items[3]) > 0:
            project_data_form.field_2.label.text = project_items[3]
            project_data_form.field_2.data = project_datas[0].field_2
    if len(project_items) > 4:
        if len(project_items[4]) > 0:
            project_data_form.field_3.label.text = project_items[4]
            project_data_form.field_3.data = project_datas[0].field_3
    if len(project_items) > 5:
        if len(project_items[5]) > 0:
            project_data_form.field_4.label.text = project_items[5]
            project_data_form.field_4.data = project_datas[0].field_4
    if len(project_items) > 6:
        if len(project_items[6]) > 0:
            project_data_form.field_5.label.text = project_items[6]
            project_data_form.field_5.data = project_datas[0].field_5
    if len(project_items) > 7:    
        if len(project_items[7]) > 0:
            project_data_form.field_6.label.text = project_items[7]
            project_data_form.field_6.data = project_datas[0].field_6
    if len(project_items) > 8:
        if len(project_items[8]) > 0:
            project_data_form.field_7.label.text = project_items[8]
            project_data_form.field_7.data = project_datas[0].field_7
    if len(project_items) > 9:
        if len(project_items[9]) > 0:
            project_data_form.field_8.label.text = project_items[9]
            project_data_form.field_8.data = project_datas[0].field_8
    if len(project_items) > 10:
        if len(project_items[10]) > 0:
            project_data_form.field_9.label.text = project_items[10]
            project_data_form.field_9.data = project_datas[0].field_9
    if len(project_items) > 11:
        if len(project_items[11]) > 0:
            project_data_form.field_10.label.text = project_items[11]
            project_data_form.field_10.data = project_datas[0].field_10
    if len(project_items) > 12:
        if len(project_items[12]) > 0:
            project_data_form.field_11.label.text = project_items[12]
            project_data_form.field_11.data = project_datas[0].field_11
    if len(project_items) > 13:
        if len(project_items[13]) > 0:
            project_data_form.field_12.label.text = project_items[13]
            project_data_form.field_12.data = project_datas[0].field_12
    if len(project_items) > 14:
        if len(project_items[14]) > 0:
            project_data_form.field_13.label.text = project_items[14]
            project_data_form.field_13.data = project_datas[0].field_13
    if len(project_items) > 15:
        if len(project_items[15]) > 0:
            project_data_form.field_14.label.text = project_items[15]
            project_data_form.field_14.data = project_datas[0].field_14
    if len(project_items) > 16:
        if len(project_items[16]) > 0:
            project_data_form.field_15.label.text = project_items[16]
            project_data_form.field_15.data = project_datas[0].field_15
    if len(project_items) > 17:
        if len(project_items[17]) > 0:
            project_data_form.field_16.label.text = project_items[17]
            project_data_form.field_16.data = project_datas[0].field_16
    if len(project_items) > 18:
        if len(project_items[18]) > 0:
            project_data_form.field_17.label.text = project_items[18]
            project_data_form.field_17.data = project_datas[0].field_17
    if len(project_items) > 19:
        if len(project_items[19]) > 0:
            project_data_form.field_18.label.text = project_items[19]
            project_data_form.field_18.data = project_datas[0].field_18
    if len(project_items) > 20:
        if len(project_items[20]) > 0:
            project_data_form.field_19.label.text = project_items[20]
            project_data_form.field_19.data = project_datas[0].field_19
    if len(project_items) > 21:
        if len(project_items[21]) > 0:
            project_data_form.field_20.label.text = project_items[21]
            project_data_form.field_20.data = project_datas[0].field_20
    if len(project_items) > 22:
        if len(project_items[22]) > 0:
            project_data_form.field_21.label.text = project_items[22]
            project_data_form.field_21.data = project_datas[0].field_21
    reports = ProjectTab.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', per_page_default, type=int)

    clear_session = request.args.get('clear', 0, type=int)
    find_count = 0
    find_count = ProjectTab.query.count()

    session['per_page'] = per_page_default
    if per_page != per_page_default:
        session['per_page'] = per_page
    
    return render_template('update_data.html', log_id=log_id,form=search_form,project_name=project_name,project_items=project_items, project_data=project_datas[0],  select_item=select_item, search_input=search_input,project_data_form=project_data_form,projects=projects)    