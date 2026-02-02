from app.extensions import db

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    stdnum = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(100), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('student_course.id'), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='ACTIVE'
    ) 

    attendance_logs = db.relationship(
        'EntryLog',  # string reference is fine
        back_populates='student',
        lazy=True
    )
    course_rel = db.relationship(
        'StudentCourse',
        back_populates='students',  # match this in StudentCourse
        lazy=True
    )
    def __repr__(self):
        return f'<User {self.username}>'
    
class StudentCourse(db.Model):
    __tablename__ = 'student_course'
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

    
    students = db.relationship(
        'Student',
        back_populates='course_rel',  # match the attribute in Student
        lazy=True
    )

    def __repr__(self):
        return f'<StudentCourse {self.name}>'