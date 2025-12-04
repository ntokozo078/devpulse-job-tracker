from app import create_app, db
from app.models import JobPosting, Skill

# Initialize the app to access the database
app = create_app()

def get_or_create_skill(skill_name):
    """
    Helper function to manage Skills.
    If 'Python' exists, return the object.
    If 'Python' does not exist, create it, add it to DB, and return it.
    """
    # 1. Check if skill exists
    skill = Skill.query.filter_by(name=skill_name).first()
    
    # 2. If not, create it
    if not skill:
        skill = Skill(name=skill_name)
        db.session.add(skill)
        # We flush to get the ID immediately, but commit later
        db.session.flush() 
    
    return skill

def load_jobs_to_db(cleaned_jobs):
    """
    Takes a list of cleaned job dictionaries and saves them to the database.
    """
    print(f"--- Loading {len(cleaned_jobs)} jobs into the database ---")
    
    # We must push the application context to interact with Flask-SQLAlchemy
    with app.app_context():
        new_count = 0
        skipped_count = 0
        
        for job_data in cleaned_jobs:
            # 1. Check for Duplicates
            # We use the URL as a unique identifier
            existing_job = JobPosting.query.filter_by(url=job_data['url']).first()
            if existing_job:
                skipped_count += 1
                continue # Skip this job, we already have it

            # 2. Create the Job Object
            new_job = JobPosting(
                title=job_data['title'],
                company=job_data['company'],
                location=job_data['location'],
                is_remote=job_data['is_remote'],
                salary_min=job_data['salary_min'],
                salary_max=job_data['salary_max'],
                currency=job_data['currency'],
                url=job_data['url'],
                source_site=job_data['source_site'],
                description=job_data['description'],
                date_posted=job_data['date_posted']
            )

            # 3. Handle Relationships (The "Software Engineering" part)
            # We loop through the list of skill strings ['Python', 'SQL']
            # and convert them into actual Database Objects
            for skill_name in job_data['skills']:
                skill_obj = get_or_create_skill(skill_name)
                new_job.skills.append(skill_obj)

            # 4. Add to Session
            db.session.add(new_job)
            new_count += 1

        # 5. Commit all changes
        try:
            db.session.commit()
            print(f"SUCCESS: Added {new_count} new jobs. Skipped {skipped_count} duplicates.")
        except Exception as e:
            db.session.rollback()
            print(f"CRITICAL ERROR during loading: {e}")

# --- Test Block ---
if __name__ == "__main__":
    # Fake cleaned data to test the loader
    fake_cleaned = [{
        'title': 'Test Loader Job',
        'company': 'LoadCorp',
        'location': 'Cape Town',
        'is_remote': True,
        'salary_min': 50000,
        'salary_max': 70000,
        'currency': 'ZAR',
        'url': 'http://load-test.com/1',
        'source_site': 'Test',
        'description': 'Test Description',
        'date_posted': None,
        'skills': ['Python', 'PostgreSQL'] # Note: PostgreSQL might be a new skill
    }]
    
    load_jobs_to_db(fake_cleaned)