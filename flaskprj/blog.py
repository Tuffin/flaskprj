import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from flaskprj.models import db, Post, User
from flaskprj.auth import login_required

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Post).order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['FLASKPRJ_POST_PER_PAGE'], error_out=False
    )
    # posts = db.session.query(Post).order_by(Post.created.desc()).all()
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, 
                        author_id=g.user.id, modified=False, created=datetime.datetime.now())
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = db.session.query(Post).filter(Post.id == id).one_or_none()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = db.session.query(Post).filter(Post.id == id).one()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            modify_time = datetime.datetime.now()
            modified = True
            post.title = title
            post.body = body
            post.modified = modified
            post.modify_time = modify_time
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
