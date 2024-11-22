# Web Scraper and Prompt Generator

This is a Flask-based web application that combines web scraping capabilities with AI-powered prompt generation. Users can scrape web content and generate prompts using advanced language models.

## Featuresve

- User authentication (local and Google OAuth)
- Web scraping functionality
- AI-powered prompt generation
- Dashboard to view scraped data and generated prompts

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package manager)
- PostgreSQL database

 Installation

1. Clone the repository: https://github.com/Kartikey1306/IDE-Host-Private-Limited.git

2. Set up a virtual environment**:
python -m venv venv
source venv/bin/activate  # On Windows, use `nv\Scripts\activate`



3. Install required packages**:
pip install -r requirements.txt


4. Initialize the database**:
flask db init
flask db migrate
flask db upgrade



5. Run the application**:
flask run
