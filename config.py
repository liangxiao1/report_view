import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'simple report viewer'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'report_data.db')
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True

config = {
    'development': DevelopmentConfig,
    'production': Config,
    'default': DevelopmentConfig
}