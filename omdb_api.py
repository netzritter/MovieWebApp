import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file (only needed in local/dev)

OMDB_API_KEY = os.getenv('OMDB_API_KEY')  # ✅ Secure!

def fetch_movie_data(title):
    try:
        url = f'http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'name': data.get('Title'),
                'director': data.get('Director'),
                'year': int(data.get('Year')) if data.get('Year') and data['Year'].isdigit() else None,
                'rating': float(data.get('imdbRating')) if data.get('imdbRating') != 'N/A' else None
            }
    except Exception as e:
        print(f"[OMDb Error] {e}")
    return None
