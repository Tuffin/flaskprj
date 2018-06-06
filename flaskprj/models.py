import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import current_app

db = SQLAlchemy()

class Permission:
    WRITE = 1
    ADMIN = 2


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    # default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.WRITE],
            'Administrator': [Permission.WRITE, Permission.ADMIN]
        }
        for r in roles:
            # role = Role.query.filter_by(name==r).first()
            role = db.session.query(Role).filter(Role.name==r).first()
            if not role:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            db.session.add(role)
        db.session.commit()


    def has_permission(self, perm):
        return self.permission & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permission += perm

    def rm_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm

    def reset_permission(self):        
        self.permission = 0

    def __repr__(self):
        return '<Role %s>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    post = db.relationship('Post', backref='user', lazy=True)

    @property
    def is_authenticated(self):
        return self.role.name == 'Administrator'

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
        if self.role is None:
            if self.username == current_app.config['FLASKPRJ_ADMIN']:
                self.role = db.session.query(Role).filter(Role.name=='Administrator').first()
                # self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = db.session.query(Role).filter(Role.name=='User').first()

    def __repr__(self):
        return '<User %s>' % self.username


tag_post = db.Table('tag_post',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    modified = db.Column(db.Boolean, nullable=False, default=False)
    modify_time = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tag_post, backref=db.backref('posts', lazy='dynamic'), lazy=True)

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<Post %s>' % self.title

    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)
        return self

    def remove_tag(self, tag):
        if self.has_tag(tag):
            self.tags.remove(tag)
        return self
    
    def has_tag(self, tag):
        if tag.id is None:
            return False
        # return self.tags.filter(tag_post.c.tag_id==tag.id).first() is not None
        return tag in self.tags


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text)

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<Profile %s>' % self.id


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<Tag %s>' % self.name
