from app.extensions import db
from datetime import datetime

class Borrow(db.Model):
    __tablename__ = 'borrow'
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.id'), nullable=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest_borrower.id'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    returned_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='BORROWED')

    student = db.relationship('Student', backref='borrowed_books', lazy=True)
    borrower = db.relationship('Borrower', backref='borrowed_books', lazy=True)
    guest = db.relationship('Guest', backref='borrowed_books', lazy=True)
    book = db.relationship('Book', backref='borrow_records', lazy=True)

    def __repr__(self):
        return f"<Borrow BookID:{self.book_id} by {'Student' if self.student_id else 'Borrower' if self.borrower_id else 'Guest'} ID:{self.student_id or self.borrower_id or self.guest_id}>"

    # <<< ADD THESE PROPERTIES >>>
    @property
    def borrower_type(self):
        if self.student_id:
            return 'Student'
        elif self.borrower_id:
            return 'Borrower'
        elif self.guest_id:
            return 'Guest'
        return 'Unknown'

    @property
    def borrower_name(self):
        if self.student:
            return f"{self.student.firstname} {self.student.lastname}"
        elif self.borrower:
            return f"{self.borrower.firstname} {self.borrower.lastname}"
        elif self.guest:
            return self.guest.fullname
        return 'Unknown'
