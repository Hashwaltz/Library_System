from flask import Blueprint, render_template
from sqlalchemy import func, extract
from datetime import datetime
from app.utils.decorators import role_required
from app.models import Student, Borrower, Guest, Book, Borrow
from app.extensions import db

from . import librarian_bp


@librarian_bp.route('/dashboard')
@role_required('Librarian')
def dashboard():

    # ===============================
    # TOTAL COUNTS
    # ===============================

    total_students = Student.query.count()
    total_borrowers = Borrower.query.count()
    total_guests = Guest.query.count()

    total_users = total_students + total_borrowers + total_guests

    active_students = Student.query.filter_by(status='ACTIVE').count()
    active_borrowers = Borrower.query.filter_by(is_active=True).count()

    active_members = active_students + active_borrowers

    total_books = Book.query.filter_by(is_archived=False).count()

    total_borrowed = Borrow.query.filter_by(status='BORROWED').count()

    # ===============================
    # MONTHLY BORROWED BOOKS (Current Year)
    # ===============================

    current_year = datetime.utcnow().year

    monthly_data = (
        db.session.query(
            extract('month', Borrow.borrowed_at).label('month'),
            func.count(Borrow.id)
        )
        .filter(extract('year', Borrow.borrowed_at) == current_year)
        .group_by('month')
        .all()
    )

    # Convert to 12-month array
    monthly_borrowed = [0] * 12
    for month, count in monthly_data:
        monthly_borrowed[int(month) - 1] = count

    # ===============================
    # BORROWER TYPE DISTRIBUTION
    # ===============================

    student_count = Borrow.query.filter(Borrow.student_id.isnot(None)).count()
    borrower_count = Borrow.query.filter(Borrow.borrower_id.isnot(None)).count()
    guest_count = Borrow.query.filter(Borrow.guest_id.isnot(None)).count()

    book_status_counts = [
        student_count,
        borrower_count,
        guest_count
    ]

    # ===============================
    # TOP BORROWED BOOKS
    # ===============================

    top_books_query = (
        db.session.query(
            Book.title,
            Book.author,
            func.count(Borrow.id).label("times_borrowed")
        )
        .join(Borrow)
        .group_by(Book.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(5)
        .all()
    )

    top_borrowed_books = [
        {
            "title": book.title,
            "author": book.author,
            "times_borrowed": book.times_borrowed
        }
        for book in top_books_query
    ]

    return render_template(
        "librarian/dashboard.html",
        total_users=total_users,
        total_books=total_books,
        total_borrowed=total_borrowed,
        active_members=active_members,
        monthly_borrowed=monthly_borrowed,
        book_status_counts=book_status_counts,
        top_borrowed_books=top_borrowed_books
    )