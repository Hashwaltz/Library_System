from app.extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stdnum = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    


    def __repr__(self):
        return f'<User {self.username}>'