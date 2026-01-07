from app.extensions import db

class Borrower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(80), unique=True, nullable=True)
    lastname = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=True)
    borrower_type = db.Column(db.String(50), nullable=False)  # e.g., 'student', 'faculty', 'staff'
    department = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(120), nullable=True)
    date_hired = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Borrower {self.borrower_type} ID: {self.borrower_id}>'