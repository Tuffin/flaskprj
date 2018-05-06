from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flaskprj.auth import login_required
from flaskprj.db import get_db

bp = Blueprint('article', __name__, url_prefix='/article')


def get_article(id):
    article = get_db().excute(
        'SELECT p.id, title, body, created, author_id, username'
        'FROM post p JOIN user u ON p.id = u.id'
        'WHERE p.id = ?',
        (id,)
    ).fetchone()

    if article is None:
        abort(404, "Article id {} doesn't exist".format(id))
    
    return article


@bp.route('/article/<int:id>')
def page(id):
    article = get_article(id)
    
    render_template('article.html', article=article)
