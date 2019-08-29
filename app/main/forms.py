from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email
from .. import report_db
from .db_class import ProjectMap,ProjectTab

class LoginForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    submit = SubmitField("Login")

class NewUserForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    email = TextField('Email')
    role = SelectField('Role', choices=[('admin', 'admin'),('user', 'user')])
    submit = SubmitField("Create")

class EditUserForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    email = TextField('Email')
    role = SelectField('Role', choices=[('admin', 'admin'),('user', 'user')])
    submit = SubmitField("Update")
    cancel = SubmitField("Cancel")

class SearchForm(FlaskForm):
    search_input = TextField(
        '', render_kw={"placeholder": "Filter by what?"}, validators=[Required()])
    select_item = SelectField('', choices=[('ami_id', 'ami_id'),
                                           ('instance_type', 'instance_type'), ('compose_id',
                                                                                'compose_id'), ('pkg_ver', 'pkg_ver'),
                                           ('bug_id', 'bug_id'), ('branch_name', 'branch_name'), ('test_date', 'test_date'), ('instance_available_date', 'instance_available_date')])
    submit = SubmitField("Go")
    reset = SubmitField("Reset")

class SearchForm_v2(FlaskForm):
    search_input = TextField(
        '', render_kw={"placeholder": "Filter by what?"}, validators=[Required()])
    select_item = SelectField()
    def set_choices(self,l):
        self.select_item.choices = l
    submit = SubmitField("Go")
    reset = SubmitField("Reset")

class UpdateItemForm(FlaskForm):
    log_id = TextField('log_id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    ami_id = TextField('ami_id', render_kw={'readonly': True})
    instance_type = TextField('instance_type', render_kw={'readonly': True})
    compose_id = TextField('compose_id', render_kw={'readonly': True})
    instance_available_date = TextField('instance_available_date')
    pkg_ver = TextField('pkg_ver', render_kw={'readonly': False})
    bug_id = TextField('bug_id')
    report_url = TextField('report_url')
    branch_name = TextField('branch_name')
    cases_pass = TextField('cases_pass', render_kw={'readonly': True})
    cases_fail = TextField('cases_fail', render_kw={'readonly': True})
    cases_cancel = TextField('cases_cancel', render_kw={'readonly': True})
    cases_other = TextField('cases_other', render_kw={'readonly': True})
    cases_total = TextField('cases_total', render_kw={'readonly': True})
    pass_rate = TextField('pass_rate', render_kw={'readonly': True})
    test_date = TextField('test_date', render_kw={'readonly': True})
    comments = TextAreaField('comments')
    submit = SubmitField("Update")
    delete = SubmitField("Delete")

class ProjectForm(FlaskForm):
    project_id = TextField('project_id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    project_name = TextField('project_name')
    field_1 = TextField('field_1')
    field_2 = TextField('field_2')
    field_3 = TextField('field_3')
    field_4 = TextField('field_4')
    field_5 = TextField('field_5')
    field_6 = TextField('field_6')
    field_7 = TextField('field_7')
    field_8 = TextField('field_8')
    field_9 = TextField('field_9')
    field_10 = TextField('field_10')
    field_11 = TextField('field_11')
    field_12 = TextField('field_12')
    field_13 = TextField('field_13')
    field_14 = TextField('field_14')
    field_15 = TextField('field_15')
    field_16 = TextField('field_16')
    field_17 = TextField('field_17')
    field_18 = TextField('field_18')
    field_19 = TextField('field_19')
    field_20 = TextField('field_20')

class NewProjectForm(FlaskForm):
    project_id = TextField('project_id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    project_name = TextField('project_name')
    field_1 = TextField('field_1')
    field_2 = TextField('field_2')
    field_3 = TextField('field_3')
    field_4 = TextField('field_4')
    field_5 = TextField('field_5')
    field_6 = TextField('field_6')
    field_7 = TextField('field_7')
    field_8 = TextField('field_8')
    field_9 = TextField('field_9')
    field_10 = TextField('field_10')
    field_11 = TextField('field_11')
    field_12 = TextField('field_12')
    field_13 = TextField('field_13')
    field_14 = TextField('field_14')
    field_15 = TextField('field_15')
    field_16 = TextField('field_16')
    field_17 = TextField('field_17')
    field_18 = TextField('field_18')
    field_19 = TextField('field_19')
    field_20 = TextField('field_20')
    submit = SubmitField("Add")

class EditProjectForm(FlaskForm):
    project_id = TextField('project_id', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    project_name =  TextField('project_name', render_kw={
                    'readonly': True, 'class': "col-sm-10"})
    field_1 = TextField('field_1')
    field_2 = TextField('field_2')
    field_3 = TextField('field_3')
    field_4 = TextField('field_4')
    field_5 = TextField('field_5')
    field_6 = TextField('field_6')
    field_7 = TextField('field_7')
    field_8 = TextField('field_8')
    field_9 = TextField('field_9')
    field_10 = TextField('field_10')
    field_11 = TextField('field_11')
    field_12 = TextField('field_12')
    field_13 = TextField('field_13')
    field_14 = TextField('field_14')
    field_15 = TextField('field_15')
    field_16 = TextField('field_16')
    field_17 = TextField('field_17')
    field_18 = TextField('field_18')
    field_19 = TextField('field_19')
    field_20 = TextField('field_20')
    submit = SubmitField("Update")
    delete = SubmitField("Delete")

class ProjectDataForm(FlaskForm):
    id = TextField('id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    project_id = TextField('project_id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    project_name = TextField('project_name', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    field_1 = TextField('field_1')
    field_2 = TextField('field_2')
    field_3 = TextField('field_3')
    field_4 = TextField('field_4')
    field_5 = TextField('field_5')
    field_6 = TextField('field_6')
    field_7 = TextField('field_7')
    field_8 = TextField('field_8')
    field_9 = TextField('field_9')
    field_10 = TextField('field_10')
    field_11 = TextField('field_11')
    field_12 = TextField('field_12')
    field_13 = TextField('field_13')
    field_14 = TextField('field_14')
    field_15 = TextField('field_15')
    field_16 = TextField('field_16')
    field_17 = TextField('field_17')
    field_18 = TextField('field_18')
    field_19 = TextField('field_19')
    field_20 = TextField('field_20')
    submit = SubmitField("Add")

class EditProjectDataForm(FlaskForm):
    id = TextField('id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    project_id = TextField('project_id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    project_name = TextField('project_name', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    field_1 = TextField('field_1')
    field_2 = TextField('field_2')
    field_3 = TextField('field_3')
    field_4 = TextField('field_4')
    field_5 = TextField('field_5')
    field_6 = TextField('field_6')
    field_7 = TextField('field_7')
    field_8 = TextField('field_8')
    field_9 = TextField('field_9')
    field_10 = TextField('field_10')
    field_11 = TextField('field_11')
    field_12 = TextField('field_12')
    field_13 = TextField('field_13')
    field_14 = TextField('field_14')
    field_15 = TextField('field_15')
    field_16 = TextField('field_16')
    field_17 = TextField('field_17')
    field_18 = TextField('field_18')
    field_19 = TextField('field_19')
    field_20 = TextField('field_20')
    submit = SubmitField("Update")
    delete = SubmitField("Delete")