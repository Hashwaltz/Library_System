import os

# Absolute path to instance folder
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

class DevelopmentConfig:
    SECRET_KEY = "dev-key"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'library.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
