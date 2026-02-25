from sqlalchemy import func
from flask import render_template, request
from app.extensions import db
from app.models import Borrower, Guest, Student
from app.utils.decorators import role_required



from . import librarian_bp


#------------
#Borrowers
#------------


@role_required('Librarian')
@librarian_bp.route()
def Borrowers():
    borrowers = Borrowers.query.All()

    return render_template("librarian/borrowers.html",
                           borrowers=borrowers)
