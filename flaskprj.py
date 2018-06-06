import os
import sys
from flask_migrate import Migrate, upgrade
from flaskprj import create_app
from flaskprj.models import db, User, Post, Tag, Role, Profile

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, Tag=Tag, Profile=Profile, Role=Role)

@app.cli.command()
def deploy():
    upgrade()

    Role.insert_roles()
