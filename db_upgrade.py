#!venv/bin/python

import imp
from config import config
from flaskprj.models import db
from flaskprj import create_app
from migrate.versioning import api


SQLALCHEMY_DATABASE_URI = config['development'].SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = config['development'].SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
