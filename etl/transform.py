import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime

# 1. Define the Skill Dictionary
# These are the keywords we will search for in every job description.
# In a production app, this might live in a database table.
TARGET_SKILLS = [
    'Python', 'SQL', 'Java', 'C#', 'AWS', 'Azure', 'GCP', 
    'Docker', 'Kubernetes', 'Spark', 'Hadoop', 'Databricks',
    'Flask', 'Django', 'React', 'Power BI', 'Tableau', 'Excel'
]

def clean_html(raw_html):
    """
    Removes HTML tags (<div>, <strong>, etc.) from the text.
    """
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator=' ').strip()

def extract_skills_from_text(text):
    """
    Scans the text for target skills.
    Returns a list of unique skills found (e.g., ['Python', 'AWS']).
    """
    found_skills = []
    # Normalize text to lowercase for searching
    text_lower = text.lower()
    
    for skill in TARGET_SKILLS:
        # Use regex to find the skill as a whole word (avoids matching 'Java' inside 'JavaScript')
        # \b means "word boundary"
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
            
    return found_skills

def transform_jobs(raw_jobs_list):
    """
    Main transformation function.
    Args:
        raw_jobs_list (list): The list of dicts from Adzuna API.
    Returns:
        list: A list of cleaned, structured dictionaries ready for the DB.
    """
    cleaned_data = []

    print(f"--- Transforming {len(raw_jobs_list)} raw jobs ---")

    for job in raw_jobs_list:
        try:
            # 1. Clean the Description
            # Adzuna returns 'description' as a snippet, sometimes full text is hard to get via API
            # We work with what we have.
            raw_desc = job.get('description', '')
            clean_desc = clean_html(raw_desc)
            
            # 2. Extract Skills
            # We combine title and description to improve detection chances
            full_text = f"{job.get('title', '')} {clean_desc}"
            skills_found = extract_skills_from_text(full_text)
            
            # 3. Normalize Salary
            # Adzuna gives min/max. We store them, but sometimes they are 0 or None.
            s_min = job.get('salary_min')
            s_max = job.get('salary_max')
            
            # 4. Normalize Date
            # Adzuna format: "2024-01-05T12:00:00Z" -> Python datetime object
            date_str = job.get('created', datetime.utcnow().isoformat())
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                date_obj = datetime.utcnow()

            # 5. Build the Clean Object
            clean_job = {
                'title': job.get('title', 'Unknown Title'),
                'company': job.get('company', {}).get('display_name', 'Unknown Company'),
                'location': job.get('location', {}).get('display_name', 'South Africa'),
                'is_remote': 1 if 'remote' in full_text.lower() else 0, # Simple detection
                'salary_min': s_min,
                'salary_max': s_max,
                'currency': 'ZAR', # API Default for 'za' endpoint
                'url': job.get('redirect_url'),
                'source_site': 'Adzuna',
                'description': clean_desc,
                'date_posted': date_obj,
                'skills': skills_found  # List of strings ['Python', 'SQL']
            }
            
            cleaned_data.append(clean_job)
            
        except Exception as e:
            print(f"WARNING: Error transforming job: {e}")
            continue

    print(f"SUCCESS: Transformed {len(cleaned_data)} jobs.")
    return cleaned_data

# --- Test Block ---
if __name__ == "__main__":
    # Fake raw data to test the logic without calling the API
    fake_raw = [{
        "title": "Junior Data Engineer",
        "company": {"display_name": "TestCorp"},
        "location": {"display_name": "Durban"},
        "description": "<strong>Must know Python and Azure.</strong>",
        "salary_min": 30000,
        "salary_max": 45000,
        "redirect_url": "http://test.com",
        "created": "2023-12-01T10:00:00Z"
    }]
    
    result = transform_jobs(fake_raw)
    print("\n--- TRANSFORMATION RESULT ---")
    print(result[0]['skills']) # Should print ['Python', 'Azure']