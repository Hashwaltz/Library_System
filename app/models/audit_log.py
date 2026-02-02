from app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # The admin who performed the action
    action = db.Column(db.String(100), nullable=False)  # e.g., "ADD STUDENT", "EDIT FACULTY"
    table_name = db.Column(db.String(100), nullable=False)  # e.g., "student", "borrower"
    record_id = db.Column(db.Integer, nullable=True)  # ID of the record affected
    old_data = db.Column(db.Text, nullable=True)  # JSON string for previous data
    new_data = db.Column(db.Text, nullable=True)  # JSON string for new data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.table_name} ID {self.record_id}>"
