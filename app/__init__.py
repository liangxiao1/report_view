from datetime import timedelta, date, datetime
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_

#from .main.forms import LoginForm, SearchForm, UpdateItemForm

from flask_login import LoginManager, login_user, login_required, current_user, UserMixin, logout_user

from bs4 import BeautifulSoup
import urllib2
from flask_googlecharts import GoogleCharts, ColumnChart, BarChart, LineChart
from config import config

bootstrap = Bootstrap()
report_db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
charts = GoogleCharts()

#bp = Blueprint('report', __name__, url_prefix='/report')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    report_db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    charts.init_app(app)

    return app
