from flask  import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.student import Student, StudentCourse
from app.models.entry_log import EntryLog
from app.models.book import Book
from sqlalchemy import func
from app.utils.decorators import role_required


from . import admin_bp


@admin_bp.route('/reports')
@role_required("Admin")
def reports_dashboard():
    return render_template('admin/reports/dashboard.html')



@admin_bp.route('/reports/attendance')
@role_required("Admin")
def attendance_report():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # number of records per page

    pagination = db.session.query(
        EntryLog,
        Student
    ).join(Student, EntryLog.student_id == Student.id
    ).order_by(EntryLog.timestamp.desc()
    ).paginate(page=page, per_page=per_page)

    records = pagination.items

    return render_template('admin/reports/attendance.html',
                           records=records,
                           pagination=pagination)

@admin_bp.route('/reports/books')
@role_required("Admin")
def book_report():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # number of records per page

    pagination = db.session.query(
        Book,
        func.count(EntryLog.id).label('usage_count')
    ).outerjoin(EntryLog, EntryLog.book_id == Book.id
    ).group_by(Book.id
    ).order_by(func.count(EntryLog.id).desc()
    ).paginate(page=page, per_page=per_page)

    records = pagination.items

    return render_template('admin/reports/book_usage.html',
                           records=records,
                           pagination=pagination)


@admin_bp.route('/reports/student')
@role_required("Admin")
def student_report():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # number of records per page

    pagination = db.session.query(
        Student,
        func.count(EntryLog.id).label('log_count')
    ).outerjoin(EntryLog, EntryLog.student_id == Student.id
    ).group_by(Student.id
    ).order_by(func.count(EntryLog.id).desc()
    ).paginate(page=page, per_page=per_page)

    records = pagination.items

    return render_template('admin/reports/student_activity.html',
                           records=records,
                           pagination=pagination)



