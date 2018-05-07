from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from flaskprj.auth import login_required
from flaskprj.db import get_db

bp = Blueprint('article', __name__, url_prefix='/article')


def get_article(id):
    article = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, modified, modify_time'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if article is None:
        abort(404, "Article id {} doesn't exist".format(id))
    
    return article


@bp.route('/<int:id>')
def page(id):
    article = get_article(id)
    
    return render_template('blog/article_page.html', article=article)
