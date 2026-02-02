from app.extensions import db
from app.models.audit_log import AuditLog
from flask_login import current_user
import json


def log_audit(action, table_name, record_id=None, old_data=None, new_data=None, user_id=None):
    if user_id is None:
        user_id = getattr(current_user, "id", None)
    entry = AuditLog(
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_data=json.dumps(old_data) if old_data else None,
        new_data=json.dumps(new_data) if new_data else None,
    )
    db.session.add(entry)
    db.session.commit()