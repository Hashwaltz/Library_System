class ProductionConfig:
    SECRET_KEY = "prod-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///library_prod.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
