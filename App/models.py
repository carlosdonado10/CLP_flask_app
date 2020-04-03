from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hast = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

class Dispatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.column(db.JSON)
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<post {self.body}>'