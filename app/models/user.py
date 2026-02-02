from app.extensions import db
from sqlalchemy.sql import expression

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(
        db.Boolean,
        nullable=False,
        server_default=expression.true()
    )

    def __repr__(self):
        return f'<User {self.username}>'