from app.models import Notification
from app.extensions import db

def create_notification(title, message, role):
    notif = Notification(
        title=title,
        message=message,
        user_role=role
    )
    db.session.add(notif)
    db.session.commit()