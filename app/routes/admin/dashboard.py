from flask import Blueprint, render_template
from app.utils.decorators import role_required
from app.models.entry_log import EntryLog
from app.models.student import Student
from app.models.borrowers import Borrower, Guest
from app.models.user import User
from app.extensions import db
from app.models.book import Book
from app.models.borrow import Borrow
from sqlalchemy import func



from . import admin_bp

@admin_bp.route("/dashboard")
@role_required("Admin")
def dashboard():
    # -------------------
    # Metrics
    # -------------------
    total_users = Student.query.count() + Borrower.query.count() + Guest.query.count()
    total_books = Book.query.count()
    total_borrowed = Borrow.query.count()
    active_members = Student.query.filter_by(status='ACTIVE').count() + Borrower.query.filter_by(is_active=True).count()

    # -------------------
    # Monthly Borrowed Books
    # -------------------
    monthly_borrowed = []
    for month in range(1, 13):
        # SQLite uses strftime for extracting month
        count = Borrow.query.filter(func.strftime('%m', Borrow.borrowed_at) == f"{month:02d}").count()
        monthly_borrowed.append(count)

    # -------------------
    # Book Status Distribution
    # -------------------
    # Count by student courses
    bscs_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.course == 'BSCS').count()
    beed_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.course == 'BEED').count()
    bshm_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.course == 'BSHM').count()
    bsed_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.course == 'BSED').count()
    alumni_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.status == 'ALUMNI').count()
    faculty_count = Borrow.query.join(Borrower, Borrow.borrower_id == Borrower.id).count()

    book_status_counts = [bscs_count, beed_count, bshm_count, bsed_count, alumni_count, faculty_count]

    # -------------------
    # Top Borrowed Books
    # -------------------
    top_borrowed_books = (
        db.session.query(
            Book.title,
            Book.author,
            func.count(Borrow.id).label('times_borrowed')
        )
        .join(Borrow, Borrow.book_id == Book.id)
        .group_by(Book.id)
        .order_by(func.count(Borrow.id).desc())
        .limit(10)
        .all()
    )

    # -------------------
    # Render template
    # -------------------
    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_books=total_books,
        total_borrowed=total_borrowed,
        active_members=active_members,
        monthly_borrowed=monthly_borrowed,
        book_status_counts=book_status_counts,
        top_borrowed_books=top_borrowed_books
    )


@admin_bp.route("/borrowers")
@role_required("Admin")
def borrowers():
    return render_template("admin/borrowers.html")