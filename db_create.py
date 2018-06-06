#!venv/bin/python

import os

from config import config
from flaskprj.models import db
from migrate.versioning import api

from flaskprj import create_app
from flaskprj.models import Role
from sqlite3 import OperationalError

app = create_app()
app.app_context().push()
db.create_all()

try:
    app = create_app()
    app.app_context().push()
    Role.insert_roles()
except OperationalError:
    pass

sqluri = config[os.getenv('FLASK_CONFIG') or 'default'].SQLALCHEMY_DATABASE_URI
sqlmr = config[os.getenv('FLASK_CONFIG') or 'default'].SQLALCHEMY_MIGRATE_REPO

if not os.path.exists(sqlmr):
    api.create(sqlmr, 'database_repository')
    api.version_control(sqluri, sqlmr)
else:
    api.version_control(sqluri, sqlmr, api.version(sqlmr))
