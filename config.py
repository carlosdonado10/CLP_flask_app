import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Nunca-lo-sabremos'
    SQLALCHEMY_DATABASE_URI = 'jdbc:mysql://localhost:3306/clp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
