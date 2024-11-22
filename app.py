from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, ScrapedData, PromptLog, OAuth

google_blueprint = make_google_blueprint(
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scope=['profile', 'email'],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)
app.register_blueprint(google_blueprint, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", category="error")
        return False

    google_info = resp.json()
    google_user_id = google_info["id"]

    existing_user = User.query.filter_by(email=google_info["email"]).first()

    if existing_user:
        login_user(existing_user)
        flash("Successfully signed in with Google.", category="success")
    else:
        new_user = User(
            name=google_info["name"],
            email=google_info["email"],
            social_login_provider="google"
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Successfully signed up with Google.", category="success")

    return redirect(url_for("dashboard"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    scraped_data = ScrapedData.query.filter_by(user_id=current_user.id).all()
    prompts = PromptLog.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', scraped_data=scraped_data, prompts=prompts)

if __name__ == '__main__':
    app.run(debug=True)

