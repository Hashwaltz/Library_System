from app.extensions import db
from datetime import datetime, date
from typing import List


class Borrow(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=True
    )

    borrower_id = db.Column(
        db.Integer,
        db.ForeignKey('borrower.id'),
        nullable=True
    )

    guest_id = db.Column(
        db.Integer,
        db.ForeignKey('guest_borrower.id'),
        nullable=True
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey('book.id'),
        nullable=False
    )

    borrowed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    returned_at = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default='BORROWED'
    )

    days_late = db.Column(
        db.Integer,
        default=0
    )

    # Relationships
    student = db.relationship(
        'Student',
        backref=db.backref('borrow_records_student', lazy=True)
    )

    borrower = db.relationship(
        'Borrower',
        foreign_keys=[borrower_id],
        back_populates='borrowed_books'
    )

    guest = db.relationship(
        'Guest',
        backref=db.backref('borrow_records_guest', lazy=True)
    )
    book = db.relationship(
        'Book',
        backref='borrow_records',
        lazy=True
    )

    violations = db.relationship(
        "Violation",
        back_populates="borrow_record",
        lazy=True
    )

    def __repr__(self):
        borrower_id = self.student_id or self.borrower_id or self.guest_id

        borrower_type = (
            'Student' if self.student_id else
            'Borrower' if self.borrower_id else
            'Guest'
        )

        return f"<Borrow BookID:{self.book_id} {borrower_type} ID:{borrower_id}>"

    # Validation Helper ⭐
    def validate_borrower(self):
        return sum([
            self.student_id is not None,
            self.borrower_id is not None,
            self.guest_id is not None
        ]) == 1



class ViolationType(db.Model):
    __tablename__ = 'violation_type'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    severity_level = db.Column(
        db.Integer,
        default=1
    )

    description = db.Column(
        db.String(255)
    )

    violations = db.relationship(
        'Violation',
        backref=db.backref('violation_type_rel', lazy=True),
        lazy=True
    )

class Violation(db.Model):
    __tablename__ = 'violation'

    id = db.Column(db.Integer, primary_key=True)

    violation_type_id = db.Column(
        db.Integer,
        db.ForeignKey('violation_type.id'),
        nullable=False
    )

    borrow_id = db.Column(
        db.Integer,
        db.ForeignKey('borrow.id'),
        nullable=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('student.id'),
        nullable=True
    )

    borrower_id = db.Column(
        db.Integer,
        db.ForeignKey('borrower.id'),
        nullable=True
    )

    guest_id = db.Column(
        db.Integer,
        db.ForeignKey('guest_borrower.id'),
        nullable=True
    )

    description = db.Column(db.String(255))

    is_resolved = db.Column(
        db.Boolean,
        default=False
    )

    date_recorded = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    student = db.relationship(
        'Student',
        backref=db.backref('student_violations', lazy=True)
    )

    borrower = db.relationship(
        'Borrower',
        backref=db.backref('borrower_violations', lazy=True)
    )

    guest = db.relationship(
        'Guest',
        backref=db.backref('guest_violations', lazy=True)
    )

    borrow_record = db.relationship(
        'Borrow',
        back_populates='violations'
    )