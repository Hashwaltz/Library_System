from app.extensions import db
from datetime import datetime


class EntryLog(db.Model):
    __tablename__ = 'entry_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest_borrower.id', name='fk_entrylog_guest_id'), nullable=True)
    reason = db.Column(db.String(250), nullable=True)
    status = db.Column(db.Enum("IN", "OUT", name="entry_status"), default="IN", nullable=False)

    student = db.relationship(
        'Student',   # string reference works even if in another file
        back_populates='attendance_logs'
    )
    borrower = db.relationship('Borrower', back_populates='attendance_logs')
    guest = db.relationship('Guest', backref='attendance_logs')



