from flask import Blueprint, render_template, request, jsonify
from app.models import JobPosting, Skill, PipelineLog
from app import db
from sqlalchemy import func
import datetime

# ETL Imports
from etl.extract import extract_jobs
from etl.transform import transform_jobs
from etl.load import load_jobs_to_db

# Define the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    # 1. Search Logic
    query = request.args.get('q') 
    
    base_query = JobPosting.query
    
    if query:
        search_filter = f"%{query}%"
        jobs = base_query.filter(
            (JobPosting.title.ilike(search_filter)) | 
            (JobPosting.description.ilike(search_filter))
        ).order_by(JobPosting.date_posted.desc()).all()
    else:
        # Show top 50 recent jobs
        jobs = base_query.order_by(JobPosting.date_posted.desc()).limit(50).all()

    # 2. Stats
    total_jobs = JobPosting.query.count()
    total_skills = Skill.query.count()

    # 3. Chart Data
    top_skills_data = db.session.query(
        Skill.name, func.count(Skill.id)
    ).join(Skill.jobs).group_by(Skill.id).order_by(func.count(Skill.id).desc()).limit(5).all()
    
    skill_labels = [s[0] for s in top_skills_data]
    skill_counts = [s[1] for s in top_skills_data]

    # PASS 'jobs' TO TEMPLATE
    return render_template('dashboard.html', 
                           jobs=jobs, 
                           total_jobs=total_jobs, 
                           total_skills=total_skills,
                           search_query=query,
                           skill_labels=skill_labels,
                           skill_counts=skill_counts)

@main_bp.route('/pipeline-status')
def pipeline_status():
    logs = PipelineLog.query.order_by(PipelineLog.run_date.desc()).limit(10).all()
    return render_template('pipeline_status.html', logs=logs)

# --- NEW ROUTE FOR REMOTE TRIGGER ---
@main_bp.route('/admin/run-pipeline')
def trigger_pipeline():
    """
    A secret route to force the ETL pipeline to run from the browser.
    """
    # Categories to search
    categories = ["Software Engineer", "Data Scientist", "IT Support"]
    
    log_details = []
    total_count = 0

    try:
        # Loop through categories just like run_pipeline.py
        for cat in categories:
            # 1. Extract
            raw_data = extract_jobs(query=cat, location="South Africa")
            if not raw_data:
                log_details.append(f"{cat}: No data")
                continue
            
            # 2. Transform
            clean_data = transform_jobs(raw_data)
            
            # 3. Load
            load_jobs_to_db(clean_data)
            count = len(clean_data)
            total_count += count
            log_details.append(f"{cat}: {count} jobs")

        # 4. Log Success to DB
        new_log = PipelineLog(
            status='Success',
            jobs_found=total_count,
            details=", ".join(log_details)
        )
        db.session.add(new_log)
        db.session.commit()

        return {
            "status": "success", 
            "message": f"Pipeline finished. Found {total_count} jobs.",
            "details": log_details
        }, 200

    except Exception as e:
        # Log Failure
        error_log = PipelineLog(
            status='Failed',
            jobs_found=0,
            details=str(e)
        )
        db.session.add(error_log)
        db.session.commit()
        return {"status": "error", "message": str(e)}, 500