import os

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration settings for the Flask application.
    """
    # 1. Security Key
    # Used for signing session cookies and protecting against CSRF attacks.
    # In production, this should be a complex random string loaded from environment variables.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'devpulse-secret-key-2025'

    # 2. Database URI
    # This tells Flask where to find the database. 
    # It defaults to a local 'devpulse.db' SQLite file if a Postgres URL isn't found.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'devpulse.db')

    # Disable a feature of Flask-SQLAlchemy that signals the application every time a change is made to the DB.
    # We disable it to save memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False