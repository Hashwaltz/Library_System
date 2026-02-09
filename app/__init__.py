from flask import Flask
from .extensions import db, migrate
from flask_login import LoginManager
import os

login_manager = LoginManager()
login_manager.login_view = "auth.staff_login"
login_manager.login_message_category = "info"

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name="development"):
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
    login_manager.init_app(app)

    # Import models (so SQLAlchemy sees them)
    from .models import Book, User, Student, Borrower

    # Register blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    return app
