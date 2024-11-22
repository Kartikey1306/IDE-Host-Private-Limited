import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OAUTHLIB_INSECURE_TRANSPORT = '1'  # For development only, remove in production
    OAUTHLIB_RELAX_TOKEN_SCOPE = '1'

