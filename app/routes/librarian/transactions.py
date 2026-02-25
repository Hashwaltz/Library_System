from app.models import Book, Borrow, Borrower, Guest, Student
from app.extensions import db
from flask import request, render_template
from app.utils.decorators import role_required


from . import librarian_bp


@librarian_bp.route('/borrowing')
@role_required('Librarian')
def view_borring():
    books= Book.query.all()
    return render_template('librarian/')

