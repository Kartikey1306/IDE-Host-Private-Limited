from flask import Blueprint, render_template
from flask_login import login_required
from modules.web_application.models.scraped_data import ScrapedData
from modules.web_application.models.prompt_log import PromptLog

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    scraped_data = ScrapedData.query.filter_by(created_by_user_id=current_user.id).all()
    prompts = PromptLog.query.filter_by(created_by_user_id=current_user.id).all()
    return render_template('dashboard.html', scraped_data=scraped_data, prompts=prompts)

