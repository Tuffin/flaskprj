import datetime
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from sqlalchemy import and_
from flask_login import current_user
from werkzeug.exceptions import abort
from flask_login import login_required

from . import main
from .forms import CreateForm, UpdateForm, ProfileEditForm
from ..models import db, Post, User, Profile, Tag
from flaskprj import create_app

@main.route('/')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Post).order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['FLASKPRJ_POST_PER_PAGE'], error_out=False
    )
    posts = pagination.items

    recent_posts = db.session.query(Post).order_by(Post.created.desc()) \
        .limit(current_app.config['FLASKPRJ_RECENT_POST'])
    
    tags = db.session.query(Tag).limit(current_app.config['TAG_RANDOM_NUM'])

    return render_template('blog/index.html', posts=posts, pagination=pagination, 
                        recent_posts=recent_posts, tags=tags)


@main.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        tag_list = map(lambda x: x.strip(), list(set(form.tags.data.strip('; ').split(';')))[:5])

        post = Post(title=form.title.data, body=form.body.data, 
                    author_id=g.user.id, modified=False, created=datetime.datetime.now())
        for tag in tag_list:
            if tag:
                qtag = db.session.query(Tag).filter(Tag.name==tag).first()
                if qtag:
                    post.add_tag(qtag)
                else:
                    post.add_tag(Tag(name=tag))
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
    post = db.session.query(Post).filter(Post.id == id).one_or_none()
    if not post:
        return redirect('main.index')
    tag_list = post.tags

    form = UpdateForm()

    if form.validate_on_submit():
        tag_list = map(lambda x: x.strip(), list(set(form.tags.data.strip('; ').split(';')))[:5])
        for tag in post.tags:
            if tag.name not in tag_list:
                post.remove_tag(tag)
                if not tag.posts.count() > 0:
                    db.session.delete(tag)

        for tag in tag_list:
            if tag:
                qtag = db.session.query(Tag).filter(Tag.name==tag).first()
                if qtag:
                    post.add_tag(qtag)
                else:
                    post.add_tag(Tag(name=tag))

        modify_time = datetime.datetime.now()
        post.title = form.title.data
        post.body = form.body.data
        post.modified = True
        post.modify_time = modify_time
        db.session.commit()
        return redirect(url_for('main.index'))

    form.title.data = post.title
    form.body.data = post.body
    if tag_list:
        form.tags.data = ';'.join([tag.name for tag in tag_list])

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
    tags = article.tags

    if article is None:
        abort(404, "Article id {} doesn't exist".format(id))
    
    return article, tags


@main.route('/article/<int:id>')
def page(id):
    article, tags = get_article(id)
    
    return render_template('blog/article_page.html', article=article, tags=tags)


# @main.route('/profile/<string:username>')
# def profile(username):
#     profile = db.session.query(User, Profile).filter(
#         and_(Profile.author_id==User.id, User.username==username)).first()

#     return render_template('blog/profile.html', profile=profile, currnet_user=current_user)

@main.route('/profile')
def profile():
    profile = db.session.query(User, Profile).filter(
        and_(Profile.author_id==User.id, User.id==1)).first()

    return render_template('blog/profile.html', profile=profile, currnet_user=current_user)


@main.route('/profile-edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    user = db.session.query(User).filter(User.id==1).first()
    profile = db.session.query(Profile).filter(Profile.author_id==user.id).first()
    form = ProfileEditForm()

    if form.validate_on_submit():
        if not profile:
            profile = Profile(author_id=user.id, body=form.body.data)
            db.session.add(profile)
        else:
            profile.body = form.body.data
        db.session.commit()

        return redirect(url_for('main.profile'))
    
    if profile:
        form.body.data = profile.body

    return render_template('blog/profile_edit.html', form=form)


@main.route('/tag_<int:tag_id>')
def posts_by_tag(tag_id):
    tag = db.session.query(Tag).filter(Tag.id==tag_id).one_or_none()
    if not tag:
        return redirect('main.index')
    tag_posts = tag.posts
    tag_recent_posts = tag_posts.order_by(Post.created.desc()).limit(current_app.config['FLASKPRJ_RECENT_POST'])
    
    return render_template('blog/tag_post.html', tag=tag, tag_posts=tag_posts, tag_recent_posts=tag_recent_posts)
