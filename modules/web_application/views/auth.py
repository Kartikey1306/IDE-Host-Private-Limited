from flask import Blueprint, redirect, url_for, flash, current_app, request
from flask_dance.contrib.google import google
from flask_login import login_user, logout_user, login_required, LoginManager
from modules.web_application.models.user import User
from app import db

bp = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('auth.google_callback'))

@bp.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    return redirect(url_for('auth.google_callback'))

@bp.route('/login/google/callback')
def google_callback():
    if not google.authorized:
        flash('Failed to log in with Google.', 'error')
        return redirect(url_for('main.index'))

    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('Failed to get user info from Google.', 'error')
        return redirect(url_for('main.index'))

    user_info = resp.json()
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            social_login_provider='google',
            profile_picture=user_info.get('picture')
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    flash('Logged in successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/login/error')
def login_error():
    error = request.args.get('error', 'Unknown error occurred')
    flash(f'Login failed: {error}', 'error')
    return redirect(url_for('main.index'))

