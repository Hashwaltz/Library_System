from app.models.entry_log import EntryLog
from app.models.student import Student
from app.models.borrowers import Borrower, Guest
from app.extensions import db
from app.utils.decorators import role_required
from flask import Blueprint, render_template, request
from sqlalchemy import or_
from . import admin_bp



@admin_bp.route('/entry_logs')
@role_required("admin")
def view_logs():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    status = request.args.get("status", "", type=str)
    sort = request.args.get("sort", "desc", type=str)

    query = EntryLog.query

    # 🔍 Search (student / borrower / guest)
    if search:
        query = query.outerjoin(Student).outerjoin(Borrower).outerjoin(Guest).filter(
            or_(
                Student.first_name.ilike(f"%{search}%"),
                Student.last_name.ilike(f"%{search}%"),
                Borrower.first_name.ilike(f"%{search}%"),
                Guest.first_name.ilike(f"%{search}%"),
                EntryLog.reason.ilike(f"%{search}%")
            )
        )

    # 🟢 Filter by Status
    if status in ["IN", "OUT"]:
        query = query.filter(EntryLog.status == status)

    # 🔄 Sorting
    if sort == "asc":
        query = query.order_by(EntryLog.timestamp.asc())
    else:
        query = query.order_by(EntryLog.timestamp.desc())

    pagination = query.paginate(page=page, per_page=10)

    return render_template(
        "admin/attendance.html",
        logs=pagination.items,
        pagination=pagination,
        search=search,
        status=status,
        sort=sort
    )

