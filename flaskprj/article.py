from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskprj.models import User, Post, db
from werkzeug.exceptions import abort
from flaskprj.auth import login_required

bp = Blueprint('article', __name__, url_prefix='/article')


def get_article(id):
    article = db.session.query(Post).filter(Post.id == id).one_or_none()

    if article is None:
        abort(404, "Article id {} doesn't exist".format(id))
    
    return article


@bp.route('/<int:id>')
def page(id):
    article = get_article(id)
    
    return render_template('blog/article_page.html', article=article)
