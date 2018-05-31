# !venv/bin/python
# coding:utf-8

import os
import datetime

from .admin import BlogAdminIndexView, BlogModelView
from .models import User, Post, Tag, db

from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babelex import Babel
from config import config
from flask import Flask

admin = Admin()
babel = Babel()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[os.getenv('FLASK_CONFIG')])
    config[os.getenv('FLASK_CONFIG')].init_app(app)

    app.permanent_session_lifetime = datetime.timedelta(seconds=60 * 10)
    from flaskprj.models import db
    db.init_app(app)

    babel.init_app(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    bootstrap.init_app(app)
    login_manager.init_app(app)

    admin.init_app(app, index_view=BlogAdminIndexView())
    admin.add_view(BlogModelView(User, db.session))
    admin.add_view(BlogModelView(Post, db.session))
    admin.add_view(BlogModelView(Tag, db.session))
    file_path = os.path.join(os.path.dirname(__file__), 'static/img')
    admin.add_view(FileAdmin(file_path, '/static/img/', name='图片文件'))

    try:
        if not app.instance_path:
            os.makedirs(app.instance_path)
    except OSError:
        pass

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
