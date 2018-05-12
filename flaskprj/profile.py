from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskprj.models import User, Post, db
from auth import login_required

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def porfile():
    return None
