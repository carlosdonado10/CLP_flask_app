import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Nunca-lo-sabremos'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Lapizzameodia3A-@appdb.clnghs8r4dnk.us-east-2.rds.amazonaws.com/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

base_url = 'http://localhost:5000'