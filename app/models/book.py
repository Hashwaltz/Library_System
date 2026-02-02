from app.extensions import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    assecion_number = db.Column(db.Integer, nullable=False)
    call_number = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(120), nullable=True)
    year_published = db.Column(db.Integer, nullable=True)

    classification_id = db.Column(
        db.Integer, db.ForeignKey('classification.id'), nullable=False
    )
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True)
    subject_type_id = db.Column(db.Integer, db.ForeignKey('subject_type.id'), nullable=True)
    edition_id = db.Column(db.Integer, db.ForeignKey('edition.id'), nullable=True)


    is_archived = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    books = db.relationship('Book', backref='classification', lazy=True)

    def __repr__(self):
        return f'<Classification {self.name}>'
    


class SubjectType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    books = db.relationship('Book', backref='subject_type', lazy=True)

    def __repr__(self):
        return f'<SubjectType {self.name}>'
    

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    books = db.relationship('Book', backref='section', lazy=True)

    def __repr__(self):
        return f'<Section {self.name}>'
    
class Edition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    books = db.relationship('Book', backref='edition', lazy=True)

    def __repr__(self):
        return f'<Edition {self.name}>'