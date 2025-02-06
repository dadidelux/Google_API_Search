import os
import httpx
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def google_search(api_key, search_engine_id, query, **params):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        **params
    }

    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

# Get credentials from environment variables
api_key = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')
query = 'BALMAIN Lips Print T-Shirt in White'

search_results = []
for i in range(1, 100, 10):
    response = google_search(
        api_key=api_key,
        search_engine_id=search_engine_id,
        query=query,
        start=i
    )

    search_results.extend(response.get('items', []))

df = pd.json_normalize(search_results)
df.to_csv('google_search_results.csv', index=False)
