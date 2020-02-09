from flask import render_template, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user

from app_template.extensions import login
from app_template.models import User
from ..auth import bp


login.login_view = 'auth.login'
# login.login_message = 'Che OXYEL kyda presh'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.check_password_hash(
                request.form['password']):
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
