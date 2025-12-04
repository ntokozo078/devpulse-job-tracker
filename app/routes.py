from flask import Blueprint, render_template, request
from app.models import JobPosting, Skill, PipelineLog
from app import db
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
def dashboard():
    # --- 1. SEARCH LOGIC ---
    query = request.args.get('q') # Get the search term from URL
    
    base_query = JobPosting.query
    
    if query:
        # Filter where title OR description contains the search term
        search_filter = f"%{query}%"
        jobs = base_query.filter(
            (JobPosting.title.ilike(search_filter)) | 
            (JobPosting.description.ilike(search_filter))
        ).order_by(JobPosting.date_posted.desc()).all()
    else:
        # Default: Show all
        jobs = base_query.order_by(JobPosting.date_posted.desc()).limit(50).all()

    # --- 2. STATS ---
    total_jobs = JobPosting.query.count()
    total_skills = Skill.query.count()

    # --- 3. CHART DATA (Top 5 Skills) ---
    # SQL: SELECT name, count(*) FROM skills JOIN job_skills ... GROUP BY name ...
    top_skills_data = db.session.query(
        Skill.name, func.count(Skill.id)
    ).join(Skill.jobs).group_by(Skill.id).order_by(func.count(Skill.id).desc()).limit(5).all()
    
    # Convert to lists for Chart.js
    skill_labels = [s[0] for s in top_skills_data]
    skill_counts = [s[1] for s in top_skills_data]

    return render_template('dashboard.html', 
                           jobs=jobs, 
                           total_jobs=total_jobs, 
                           total_skills=total_skills,
                           search_query=query,
                           skill_labels=skill_labels,
                           skill_counts=skill_counts)

@main_bp.route('/pipeline-status')
def pipeline_status():
    """
    Displays the health and history of the data pipeline.
    """
    # Fetch last 10 logs
    logs = PipelineLog.query.order_by(PipelineLog.run_date.desc()).limit(10).all()
    return render_template('pipeline_status.html', logs=logs)

@main_bp.route('/seed')
def seed_database():
    # ... (Keep your existing seed logic here if you want) ...
    return "Seeding disabled for now. Run 'python run_pipeline.py' instead."