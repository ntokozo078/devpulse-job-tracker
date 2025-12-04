from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize extensions (unbound to any specific app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """
    The Application Factory.
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(config_class)

    # Bind extensions to the app instance
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register Blueprints (Routes)
    # We do the import INSIDE the function to avoid circular import errors
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Create tables automatically if they don't exist (optional, good for dev)
    with app.app_context():
        db.create_all()

    return app