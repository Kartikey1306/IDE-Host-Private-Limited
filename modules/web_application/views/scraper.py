from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from modules.web_application.models.scraped_data import ScrapedData
from app import db
import requests
from bs4 import BeautifulSoup

bp = Blueprint('scraper', __name__)

@bp.route('/scrape', methods=['POST'])
@login_required
def scrape():
    url = request.json['url']
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = soup.get_text()
        metadata = {
            'title': soup.title.string if soup.title else '',
            'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ''
        }
        
        scraped_data = ScrapedData(
            url=url,
            content=content,
            metadata=metadata,
            created_by_user_id=current_user.id
        )
        db.session.add(scraped_data)
        db.session.commit()
        
        return jsonify({'message': 'Data scraped successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/scraped-data', methods=['GET'])
@login_required
def get_scraped_data():
    scraped_data = ScrapedData.query.filter_by(created_by_user_id=current_user.id).all()
    return jsonify([{
        'id': data.id,
        'url': data.url,
        'content': data.content,
        'metadata': data.metadata,
        'created_at': data.created_at
    } for data in scraped_data])

@bp.route('/scraped-data/<int:id>', methods=['DELETE'])
@login_required
def delete_scraped_data(id):
    scraped_data = ScrapedData.query.get_or_404(id)
    if scraped_data.created_by_user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(scraped_data)
    db.session.commit()
    return '', 204

