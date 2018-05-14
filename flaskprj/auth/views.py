import datetime
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.exceptions import abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth
from ..main import main
from .. import login_manager
from ..models import db, Post, User
from .forms import LoginForm, RegistrationForm


@auth.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username==form.username.data).one_or_none()
        if user is not None or check_password_hash(user.password, form.password.data):
            login_user(user)
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

        flash('Incorrect username or password.')

    return render_template('auth/login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id==user_id).one_or_none()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
