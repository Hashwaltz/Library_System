from app.extensions import db
from sqlalchemy.sql import expression

class Borrower(db.Model):
    __tablename__ = 'borrower'

    id = db.Column(db.Integer, primary_key=True)

    employee_number = db.Column(db.String(80), unique=True, nullable=True)
    lastname = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=True)

    borrower_type = db.Column(db.String(50), nullable=False)

    department = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(120), nullable=True)

    date_hired = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.String(200), nullable=True)

    contact_number = db.Column(db.String(20), nullable=True)

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        server_default=expression.true()
    )

    # Relationships ⭐
    borrowed_books = db.relationship(
        'Borrow',
        backref=db.backref('borrower_rel', lazy=True),
        lazy=True
    )

    violations = db.relationship(
        'Violation',
        backref=db.backref('borrower_rel', lazy=True),
        lazy=True
    )

    attendance_logs = db.relationship(
        'EntryLog',
        back_populates='borrower',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Borrower {self.firstname} {self.lastname}>'




class Guest(db.Model):
    __tablename__ = 'guest_borrower'

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(250))
    designation = db.Column(db.String(100))

    borrowed_books = db.relationship(
        'Borrow',
        backref=db.backref('guest_rel', lazy=True),
        lazy=True
    )

    violations = db.relationship(
        'Violation',
        backref=db.backref('guest_rel', lazy=True),
        lazy=True
    )

    def __repr__(self):
        return f'<GuestBorrower {self.fullname}>'