import requests
import json
import os

# Base URL for Adzuna API (South Africa endpoint)
# We default to 'za' (South Africa), but this can be changed to 'gb', 'us', etc.
BASE_URL = "https://api.adzuna.com/v1/api/jobs/za/search/1"

def extract_jobs(query="data engineer", location="South Africa"):
    """
    Fetches raw job data from the Adzuna API.
    
    Args:
        query (str): The job title to search for (e.g., 'Python').
        location (str): The geographic area.
    
    Returns:
        list: A list of raw job dictionaries.
    """
    
    # 1. Get Credentials from Environment Variables (Best Practice)
    # If not set, it falls back to empty strings (which will cause a 401 error)
    app_id = os.environ.get('ADZUNA_APP_ID')
    app_key = os.environ.get('ADZUNA_APP_KEY')

    if not app_id or not app_key:
        print("ERROR: API Credentials missing. Please set ADZUNA_APP_ID and ADZUNA_APP_KEY.")
        return []

    # 2. Construct the API Parameters
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'results_per_page': 20, # How many results to fetch
        'what': query,          # Job title
        'where': location,      # Location
        'content-type': 'application/json'
    }

    try:
        print(f"--- Extracting: Searching for '{query}' in '{location}' ---")
        
        # 3. Make the HTTP Request
        response = requests.get(BASE_URL, params=params)
        
        # 4. Check status code (200 = OK)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('results', [])
            print(f"SUCCESS: Retrieved {len(jobs)} raw job postings.")
            return jobs
        else:
            print(f"FAILED: Status Code {response.status_code}")
            print(f"Response: {response.text}")
            return []

    except Exception as e:
        print(f"CRITICAL ERROR during extraction: {e}")
        return []

# --- Standalone Test Block ---
# This allows you to run 'python etl/extract.py' to test this script in isolation
if __name__ == "__main__":
    # You can temporarily hardcode your keys here for testing, 
    # BUT remove them before uploading to GitHub!
    os.environ['ADZUNA_APP_ID'] = 'YOUR_APP_ID_HERE' 
    os.environ['ADZUNA_APP_KEY'] = 'YOUR_APP_KEY_HERE'
    
    # Test the function
    raw_data = extract_jobs(query="Data Engineer", location="Johannesburg")
    
    # Print the first result to see the structure
    if raw_data:
        print("\n--- SAMPLE RAW DATA (First Item) ---")
        print(json.dumps(raw_data[0], indent=2))