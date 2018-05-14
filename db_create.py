#!venv/bin/python

import os

from config import config
from flaskprj.models import db
from migrate.versioning import api

from flaskprj import create_app

app = create_app()
app.app_context().push()
db.create_all()

sqluri = config['development'].SQLALCHEMY_DATABASE_URI
sqlmr = config['development'].SQLALCHEMY_MIGRATE_REPO

if not os.path.exists(sqlmr):
    api.create(sqlmr, 'database_repository')
    api.version_control(sqluri, sqlmr)
else:
    api.version_control(sqluri, sqlmr, api.version(sqlmr))
