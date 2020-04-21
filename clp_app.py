from application import application, db
from application.models import User, Post

@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}