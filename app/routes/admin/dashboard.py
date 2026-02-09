from flask import Blueprint, render_template
from app.utils.decorators import role_required
from app.models.entry_log import EntryLog
from app.models.student import Student, StudentCourse
from app.models.borrowers import Borrower, Guest
from app.models.user import User
from app.extensions import db
from app.models.book import Book
from app.models.borrow import Borrow
from sqlalchemy import func

from . import admin_bp

@admin_bp.route("/dashboard")
@role_required("admin")
def dashboard():
    # -------------------
    # Metrics
    # -------------------
    total_users = Student.query.count() + Borrower.query.count() + Guest.query.count()
    total_books = Book.query.count()
    total_borrowed = Borrow.query.count()
    
    # Make sure Borrower has `is_active` column in DB
    active_members = Student.query.filter_by(status='ACTIVE').count() + Borrower.query.filter_by(is_active=True).count()

    # -------------------
    # Monthly Borrowed Books
    # -------------------
    monthly_borrowed = []
    for month in range(1, 13):
        count = Borrow.query.filter(func.strftime('%m', Borrow.borrowed_at) == f"{month:02d}").count()
        monthly_borrowed.append(count)

    # -------------------
    # Book Status Distribution by Student Courses
    # -------------------
    # Get all courses dynamically
    courses = StudentCourse.query.all()
    book_status_counts = []

    for course in courses:
        count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.course_id == course.id)\
                    .count()
        book_status_counts.append({
            "course": course.abbreviation,
            "count": count
        })

    # Alumni students
    alumni_count = Borrow.query.join(Student, Borrow.student_id == Student.id)\
                    .filter(Student.status == 'ALUMNI').count()
    # Faculty / Staff Borrowers
    faculty_count = Borrow.query.join(Borrower, Borrow.borrower_id == Borrower.id).count()

    # Add alumni and faculty at the end
    book_status_counts.append({"course": "ALUMNI", "count": alumni_count})
    book_status_counts.append({"course": "FACULTY/STAFF", "count": faculty_count})

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





@admin_bp.route("/manage_borrowers")
@role_required("admin")
def manage_borrowers():
    return render_template("admin/borrowers.html")