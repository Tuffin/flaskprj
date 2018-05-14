import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable = False)
    post = db.relationship('Post', backref='user', lazy=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %s>' % self.username


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    modified = db.Column(db.Boolean, nullable=False, default=False)
    modify_time = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<Post %s>' % self.title


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<Profile %s>' % self.title
