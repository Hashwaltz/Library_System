from app.extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    assecion_number = db.Column(db.Integer, nullable=False)
    call_number = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(100), nullable=True)
    edition = db.Column(db.String(50), nullable=True)
    publisher = db.Column(db.String(120), nullable=True)
    year_published = db.Column(db.Integer, nullable=True)
    section = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'