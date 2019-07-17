from flask_sqlalchemy import BaseQuery, Pagination, SQLAlchemy
from sqlalchemy import Column, Integer, String, or_
from flask_login import UserMixin

from .. import report_db

class ProjectMap(report_db.Model):
    __tablename__ = 'project_map'
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String,unique=True)
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
    def __repr__(self):
        return '<Name % r>' % self.project_name

class ProjectTab(report_db.Model):
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

class AppUser(UserMixin, report_db.Model):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    @property
    def is_admin(self):
        if 'user' in self.role:
            return False
        elif 'admin' in self.role:
            return True
    sqlite_autoincrement = True
