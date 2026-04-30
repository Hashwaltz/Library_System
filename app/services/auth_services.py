from app.models.user import User
from werkzeug.security import check_password_hash

def authenticate_staff(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "Invalid email or password"

    if not check_password_hash(user.password_hash, password):
        return None, "Invalid email or password"

    return user, None

