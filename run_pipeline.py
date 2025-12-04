from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import PipelineLog, JobPosting
from etl.extract import extract_jobs
from etl.transform import transform_jobs
from etl.load import load_jobs_to_db
import sys
import datetime

# Define the categories we want to track
SEARCH_CATEGORIES = [
    "Software Engineer",
    "Data Scientist",
    "Cyber Security",
    "IT Support",
    "Information Systems"
]

def run():
    app = create_app()
    
    print("=========================================")
    print("   STARTING DEVPULSE DATA PIPELINE")
    print("=========================================")

    total_new_jobs = 0
    logs = []

    # We need app context to save the Log to the DB
    with app.app_context():
        try:
            for category in SEARCH_CATEGORIES:
                print(f"\n--- Processing Category: {category} ---")
                
                # 1. Extract
                raw_data = extract_jobs(query=category, location="South Africa")
                
                if not raw_data:
                    print(f"Skipping {category}: No data found.")
                    continue

                # 2. Transform
                clean_data = transform_jobs(raw_data)

                # 3. Load
                # We need to capture how many were actually added (vs duplicates)
                # Note: We are approximating here based on list size for simplicity
                load_jobs_to_db(clean_data)
                total_new_jobs += len(clean_data)

            # 4. Log Success
            log_entry = PipelineLog(
                status='Success',
                jobs_found=total_new_jobs,
                details=f"Ran categories: {', '.join(SEARCH_CATEGORIES)}"
            )
            db.session.add(log_entry)
            db.session.commit()
            print("\n>> Pipeline Logged to Database: SUCCESS")

        except Exception as e:
            # 5. Log Failure
            print(f"CRITICAL PIPELINE ERROR: {e}")
            log_entry = PipelineLog(
                status='Failed',
                jobs_found=0,
                details=str(e)
            )
            db.session.add(log_entry)
            db.session.commit()

    print("=========================================")
    print("   PIPELINE FINISHED")
    print("=========================================")

if __name__ == "__main__":
    run()