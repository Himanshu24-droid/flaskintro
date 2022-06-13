from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user
from sqlalchemy import exc

from .models import User
from .extensions import login_manager, db

bp= Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        error=None

        if not username:
            error='Username is required.'
        elif not email:
            error='Email is required.'
        elif not password:
            error='Password is required.'

        if error is None:
            try:
                user=User(username=username,email=email,password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
            except exc.IntegrityError:
                error=f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template("auth/register.html")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            login_user(user)
            error = 'Logged in Successfully'
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/login.html")

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
