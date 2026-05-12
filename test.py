from app import create_app
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        user.is_active = True

    db.session.commit()

    print("All passwords reset successfully.")