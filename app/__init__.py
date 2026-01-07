from flask import Flask
from .extensions import db, migrate
import os
 
def create_app(config_name="development"):
    # Tell Flask to use instance folder
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    if config_name == "development":
        from config.development import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Make sure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Book, User, Student, Borrower 
    # Register routes
    from .routes import register_blueprints
    register_blueprints(app)

    return app
