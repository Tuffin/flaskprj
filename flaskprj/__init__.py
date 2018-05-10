import os

from flask_sqlalchemy import SQLAlchemy
from config import config
from flask import Flask


def create_app(config_name='development', test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from flaskprj.models import db
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        if not app.instance_path:
            os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()
    # from . import db_create
    # db_create.init_db()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import article
    app.register_blueprint(article.bp)

    return app
