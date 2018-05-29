import os
import sys
from flask_migrate import Migrate, upgrade
from flaskprj import create_app
from models import db, User, Post, Tag, Profile

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, Tag=Tag, Profile=Profile)

@app.cli.command()
def deploy():
    upgrade()
