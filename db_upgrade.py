#!venv/bin/python

import imp
from config import config
from flaskprj.models import db
from flaskprj import create_app
from migrate.versioning import api


SQLALCHEMY_DATABASE_URI = config[os.getenv('FLASK_CONFIG') or 'default'].SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config[os.getenv('FLASK_CONFIG') or 'default'].SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
