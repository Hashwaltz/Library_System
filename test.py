from app import create_app  # or from run import app if you have it
from app.extensions import db

app = create_app()  # or use your app object directly

with app.app_context():
    # Now you are inside the Flask app context
    print(db.engine.table_names())  # lists all tables in your DB
