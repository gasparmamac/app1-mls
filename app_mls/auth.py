import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from .form import *
from .model import *


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = LoginManager()


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        registered = User.query.filter_by(email=form.email.data).first()
        if not registered:
            new_user = User(
                name=form.name.data,
                email=form.email.data,
                create_on=datetime.now()
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        flash("You are an existing user. Please login instead.")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email not found.')
            return redirect(url_for('auth.login'))
        elif not User.check_password(password):
            flash('Invalid password.')
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            return redirect(url_for('home'))


@auth_bp.route('/logout', methods=('GET', 'POST'))
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page')
    return redirect(url_for('auth.login'))
