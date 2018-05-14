import datetime
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from flask_login import login_required

from . import main
from .forms import CreateForm, UpdateForm
from ..models import db, Post, User

@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Post).order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['FLASKPRJ_POST_PER_PAGE'], error_out=False
    )

    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@main.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, 
                    author_id=g.user.id, modified=False, created=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('blog/create.html', form=form)


def get_post(id, check_author=True):
    post = db.session.query(Post).filter(Post.id == id).one_or_none()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@main.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = db.session.query(Post).filter(Post.id == id).one()
    form = UpdateForm()

    if form.validate_on_submit():
        modify_time = datetime.datetime.now()
        post.title = form.title.data
        post.body = form.body.data
        post.modified = True
        post.modify_time = modify_time
        db.session.commit()
        return redirect(url_for('main.index'))
        
    form.title.data = post.title
    form.body.data = post.body

    return render_template('blog/update.html', post=post, form=form)


@main.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))

# article

def get_article(id):
    article = db.session.query(Post).filter(Post.id == id).one_or_none()

    if article is None:
        abort(404, "Article id {} doesn't exist".format(id))
    
    return article


@main.route('/article/<int:id>')
def page(id):
    article = get_article(id)
    
    return render_template('blog/article_page.html', article=article)
