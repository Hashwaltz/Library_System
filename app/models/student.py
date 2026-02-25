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

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('student_course.id'),
        nullable=False
    )

    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    status = db.Column(
        db.String(20),
        default='ACTIVE',
        nullable=False
    )

    attendance_logs = db.relationship(
        'EntryLog',
        back_populates='student',
        lazy=True
    )

    course = db.relationship(
        "StudentCourse",
        back_populates="students"
    )

    def __repr__(self):
        return f"<Student {self.firstname} {self.lastname}>"
    
    
class StudentCourse(db.Model):
    __tablename__ = 'student_course'
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

    
    students = db.relationship("Student", back_populates="course")

    def __repr__(self):
        return f'<StudentCourse {self.name}>'