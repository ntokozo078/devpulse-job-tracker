from . import db
from datetime import datetime

# 1. Association Table (Many-to-Many Relationship)
job_skills = db.Table('job_skills',
    db.Column('job_id', db.Integer, db.ForeignKey('job_postings.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    is_remote = db.Column(db.Boolean, default=False)
    salary_min = db.Column(db.Float, nullable=True)
    salary_max = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), default='ZAR') 
    url = db.Column(db.String(500), unique=True, nullable=False) 
    source_site = db.Column(db.String(50), nullable=False) 
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    
    skills = db.relationship('Skill', secondary=job_skills, lazy='subquery',
        backref=db.backref('jobs', lazy=True))

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Skill {self.name}>'

class PipelineLog(db.Model):
    """
    Tracks the history of ETL runs.
    Useful for monitoring system health on the 'Pipeline Status' page.
    """
    __tablename__ = 'pipeline_logs'

    id = db.Column(db.Integer, primary_key=True)
    run_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)  # 'Success', 'Failed'
    jobs_found = db.Column(db.Integer, default=0)
    details = db.Column(db.Text, nullable=True)        # Error messages or summary

    def __repr__(self):
        return f'<Log {self.run_date} - {self.status}>'