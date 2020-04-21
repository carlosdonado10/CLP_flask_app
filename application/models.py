from datetime import datetime
from application import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


    def followed_posts(self):
        followed = db.session.query(User, Post, Dispatch).join(
            Post, Post.user_id == User.id
        ).join(
            Dispatch, Dispatch.id == Post.dispatch_id, isouter=True
        ).join(
            followers, followers.c.follower_id == self.id
        )

        own = db.session.query(User, Post, Dispatch).join(
            Post, Post.user_id == User.id
        ).join(
            Dispatch, Dispatch.id == Post.dispatch_id, isouter=True
        ).filter(User.id==self.id)

        return followed.union(own)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_num_followers(self):
        return len(db.session.query(User).join(
            followers, followers.c.followed_id == User.id
        ).filter(followers.c.followed_id==self.id).all())

    def get_num_following(self):
        return len(db.session.query(User).join(
            followers, followers.c.follower_id == User.id
        ).filter(followers.c.followed_id == self.id).all())


class Dispatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(150))
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Dispatch {self.name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(64))
    dispatch_id = db.Column(db.Integer, db.ForeignKey('dispatch.id'))

    def date_to_string(self, date):
        return str(date.year) + '-' + str(date.month) + '-' + str(date.day)

    def __repr__(self):
        return f'<post {self.body}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


