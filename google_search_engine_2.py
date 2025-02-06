import os
import httpx
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm  # Progress bar

# Load environment variables from .env file
load_dotenv()

# Google Custom Search API function
def google_search(api_key, search_engine_id, query, start):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'start': start  # Defines the pagination (1st page = 1, 2nd page = 11)
    }
    
    try:
        response = httpx.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"❌ API Error: {e}")
        return {"items": []}  # Return empty result on failure

# Get credentials from environment variables
api_key = os.getenv('GOOGLE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

# Load product list and take the first 35 products
input_csv = 'products.csv'  # Adjust filename if necessary
output_csv = 'google_search_results_r.csv'

df_products = pd.read_csv(input_csv).head(35)  # Limit to first 35 products

# Initialize a list to store search results
all_results = []

# Process each product with tqdm progress bar
for _, row in tqdm(df_products.iterrows(), total=len(df_products), desc="Searching Products"):
    product_name = row['name']
    product_code = row['product']
    brand_name = row['brandname']

    search_query = f"{product_name} {brand_name}"  # Formulate query

    # Perform API requests for Page 1 and Page 2
    for start in [1, 11]:  
        response = google_search(api_key, search_engine_id, search_query, start)

        search_results = response.get('items', [])

        # Append each result with product details
        for idx, item in enumerate(search_results, start=1):
            all_results.append({
                'product_name': product_name,
                'product_code': product_code,
                'brand_name': brand_name,
                'kind': item.get('kind'),
                'title': item.get('title'),
                'link': item.get('link'),
                'displayLink': item.get('displayLink'),
                'row_number': idx  # Rank within each search
            })

# Convert results to DataFrame
df_results = pd.DataFrame(all_results)

# Save results to CSV
df_results.to_csv(output_csv, index=False)

print(f"\n✅ Search results saved to {output_csv}")
