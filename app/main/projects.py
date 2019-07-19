from . import main
from .. import report_db,login_manager,charts

from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_

from forms import LoginForm, SearchForm,SearchForm_v2,UpdateItemForm,NewProjectForm,EditProjectForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2

from .db_class import ProjectMap,ProjectTab,AppUser
from . import libs

@main.route('/initdb', methods=['GET','POST'])
def initdb():
    try:
        #ProjectTab.__table__.create(report_db.get_engine())
        #ProjectMap.__table__.create(report_db.get_engine())
        #AppUser.__table__.drop(report_db.get_engine())
        #AppUser.__table__.create(report_db.get_engine())
        report_db.create_all()
        flash('Init db done','info')
    except Exception as err:
        flash(err,'error')
    return redirect(url_for('main.index'))

@main.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    project_form = NewProjectForm()
    search_form = SearchForm_v2(csrf_enabled=True)
    project=ProjectMap()
    project.project_name=project_form.project_name.data
    if project_form.validate_on_submit():
        project_name=project_form.project_name.data
        #if ProjectMap.query.filter_by(project_name=project_name)
        project.project_name=project_form.project_name.data
        project.field_1=project_form.field_1.data
        project.field_2=project_form.field_2.data
        project.field_3=project_form.field_3.data
        project.field_4=project_form.field_4.data
        project.field_5=project_form.field_5.data
        project.field_6=project_form.field_6.data
        project.field_7=project_form.field_7.data
        project.field_8=project_form.field_8.data
        project.field_9=project_form.field_9.data
        project.field_10=project_form.field_10.data
        project.field_11=project_form.field_11.data
        project.field_12=project_form.field_12.data
        project.field_13=project_form.field_13.data
        project.field_14=project_form.field_14.data
        project.field_15=project_form.field_15.data
        project.field_16=project_form.field_16.data
        project.field_17=project_form.field_17.data
        project.field_18=project_form.field_18.data
        project.field_19=project_form.field_19.data
        project.field_20=project_form.field_20.data
        try:
            if ProjectMap.query.filter_by(project_name=project_name).count() > 1:
                flash('Project name already exists!','error')
                return render_template('create_project.html',form=search_form,project_form=project_form)
            report_db.session.add(project)
            report_db.session.commit()
            #ProjectTab.__tablename__='project_%s'%project_name
            #ProjectTab.set_tablename('project_%s'%project_name)
            #project.__table__.create(report_db.get_engine())
            flash("Added successfully!")
            return redirect(url_for('main.view',project_name=project_name))
        except Exception as err:
            flash(err,'error')
    return render_template('create_project.html',form=search_form,project_form=project_form)


@main.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    project_name=request.args.get('project_name',None)
    if project_name == None or project_name == '':
        flash('No project name specified','warning')
        return redirect(url_for('main.index'))
    
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    if len(project) == 0 or project == None:
        flash('No project named %s' % project_name,'error')
        return redirect(url_for('main.index'))
    project_form=EditProjectForm()
    search_form = SearchForm_v2(csrf_enabled=True)
    drop_list=libs.init_droplist(project_name)
    search_form.set_choices(drop_list)
    
    if project_form.validate_on_submit():
        
        if project_form.submit.data:    
            try:
                project[0].project_id =  project_form.project_id.data
                project[0].project_name = project_form.project_name.data
                project[0].field_1 = project_form.field_1.data 
                project[0].field_2 = project_form.field_2.data 
                project[0].field_3 = project_form.field_3.data 
                project[0].field_4 = project_form.field_4.data 
                project[0].field_5 = project_form.field_5.data 
                project[0].field_6 = project_form.field_6.data 
                project[0].field_7 = project_form.field_7.data 
                project[0].field_8 = project_form.field_8.data 
                project[0].field_9 = project_form.field_9.data 
                project[0].field_10 = project_form.field_10.data 
                project[0].field_11 = project_form.field_11.data 
                project[0].field_12 = project_form.field_12.data 
                project[0].field_13 = project_form.field_13.data 
                project[0].field_14 = project_form.field_14.data 
                project[0].field_15 = project_form.field_15.data 
                project[0].field_16 = project_form.field_16.data 
                project[0].field_17 = project_form.field_17.data 
                project[0].field_18 = project_form.field_18.data 
                project[0].field_19 = project_form.field_19.data 
                project[0].field_20 = project_form.field_20.data 
                report_db.session.add(project[0])
                report_db.session.commit()
                flash('Update successfully!','info')
                return redirect(url_for('main.edit_project',project_name=project_name))
            except Exception as err:
                flash(err,'error')
        elif project_form.delete.data:
            try:
                report_db.session.delete(project[0])
                report_db.session.commit()
                flash('Deleted successfully!','info')
                return redirect(url_for('main.home'))
            except Exception as err:
                flash(err,'error')
    project= ProjectMap.query.filter_by(project_name=project_name).all()
    project_form.project_id.data = project[0].project_id
    project_form.project_name.data = project[0].project_name
    project_form.field_1.data = project[0].field_1
    project_form.field_2.data = project[0].field_2
    project_form.field_3.data = project[0].field_3
    project_form.field_4.data = project[0].field_4
    project_form.field_5.data = project[0].field_5
    project_form.field_6.data = project[0].field_6
    project_form.field_7.data = project[0].field_7
    project_form.field_8.data = project[0].field_8
    project_form.field_9.data = project[0].field_9
    project_form.field_10.data = project[0].field_10
    project_form.field_11.data = project[0].field_11
    project_form.field_12.data = project[0].field_12
    project_form.field_13.data = project[0].field_13
    project_form.field_14.data = project[0].field_14
    project_form.field_15.data = project[0].field_15
    project_form.field_16.data = project[0].field_16
    project_form.field_17.data = project[0].field_17
    project_form.field_18.data = project[0].field_18
    project_form.field_19.data = project[0].field_19
    project_form.field_20.data = project[0].field_20
    projects= ProjectMap.query.all()
    return render_template('edit_project.html',form=search_form,project_form=project_form,project_name=project_name,projects=projects)

        