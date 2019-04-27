from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, TextAreaField, SelectField


class LoginForm(FlaskForm):
    username = TextField('UserName')
    password = PasswordField('Password')
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    search_input = TextField('', render_kw={"placeholder": "Filter by what?"})
    select_item = SelectField('', choices=[('ami_id', 'ami_id'),
                                           ('instance_type', 'instance_type'), ('compose_id',
                                                                                'compose_id'), ('pkg_ver', 'pkg_ver'),
                                           ('bug_id', 'bug_id'), ('branch_name', 'branch_name'), ('test_date', 'test_date'), ('instance_available_date', 'instance_available_date')])
    submit = SubmitField("Go!")


class UpdateItemForm(FlaskForm):
    log_id = TextField('log_id', render_kw={
                       'readonly': True, 'class': "col-sm-10"})
    ami_id = TextField('ami_id', render_kw={'readonly': True})
    instance_type = TextField('instance_type', render_kw={'readonly': True})
    compose_id = TextField('compose_id', render_kw={'readonly': True})
    instance_available_date = TextField('instance_available_date')
    pkg_ver = TextField('pkg_ver', render_kw={'readonly': True})
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
