import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Nunca-lo-sabremos'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

base_url = 'http://localhost:5000'