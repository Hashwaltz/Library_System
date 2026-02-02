from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.utils.decorators import role_required
from datetime import datetime
from app.models.borrowers import Borrower

from . import admin_bp  


# -----------------------------
# FACULTY LIST VIEW
# -----------------------------
@admin_bp.route("/faculty")
@role_required("Admin")
def faculty_list():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    faculty_pagination = Borrower.query.filter_by(borrower_type='faculty')\
        .order_by(Borrower.lastname.asc())\
        .paginate(page=page, per_page=per_page)

    return render_template(
        "admin/faculty_list.html",
        faculty_pagination=faculty_pagination
    )


# -----------------------------
# ADD FACULTY
# -----------------------------
@admin_bp.route("/faculty/add", methods=["POST"])
@role_required("Admin")
def add_faculty():
    employee_number = request.form.get("employee_number").strip()
    firstname = request.form.get("firstname").strip()
    middlename = request.form.get("middlename").strip()
    lastname = request.form.get("lastname").strip()
    department = request.form.get("department").strip()
    contact = request.form.get("contact").strip()
    date_hired_str = request.form.get("date_hired")
    date_hired = None
    if date_hired_str:
    # Convert string to date object
        date_hired = datetime.strptime(date_hired_str, "%Y-%m-%d").date()
    remarks = request.form.get("remarks").strip()
    contact_number = request.form.get("contact_number").strip()

    # Validation
    if not (firstname and lastname):
        flash("Firstname and Lastname are required.", "error")
        return redirect(url_for("admin.faculty_list"))

    if employee_number and Borrower.query.filter_by(employee_number=employee_number).first():
        flash("Employee number already exists.", "error")
        return redirect(url_for("admin.faculty_list"))

    new_faculty = Borrower(
        employee_number=employee_number,
        firstname=firstname,
        middlename=middlename,
        lastname=lastname,
        borrower_type='faculty',
        department=department,
        contact=contact,
        date_hired=date_hired if date_hired else None,
        remarks=remarks,
        contact_number=contact_number
    )

    db.session.add(new_faculty)
    db.session.commit()

    flash("Faculty added successfully!", "success")
    return redirect(url_for("admin.faculty_list"))


# -----------------------------
# EDIT FACULTY
# -----------------------------
@admin_bp.route("/faculty/edit/<int:faculty_id>", methods=["POST"])
@role_required("Admin")
def edit_faculty(faculty_id):
    faculty = Borrower.query.get_or_404(faculty_id)

    employee_number = request.form.get("employee_number").strip()
    firstname = request.form.get("firstname").strip()
    middlename = request.form.get("middlename").strip()
    lastname = request.form.get("lastname").strip()
    department = request.form.get("department").strip()
    contact = request.form.get("contact").strip()
    date_hired = request.form.get("date_hired")
    remarks = request.form.get("remarks").strip()
    contact_number = request.form.get("contact_number").strip()

    # Validation
    if not (firstname and lastname):
        flash("Firstname and Lastname are required.", "error")
        return redirect(url_for("admin.faculty_list"))

    if employee_number and Borrower.query.filter(Borrower.employee_number == employee_number, Borrower.id != faculty_id).first():
        flash("Employee number already exists.", "error")
        return redirect(url_for("admin.faculty_list"))

    faculty.employee_number = employee_number
    faculty.firstname = firstname
    faculty.middlename = middlename
    faculty.lastname = lastname
    faculty.borrower_type = 'faculty'
    faculty.department = department
    faculty.contact = contact
    faculty.date_hired = date_hired if date_hired else None
    faculty.remarks = remarks
    faculty.contact_number = contact_number

    db.session.commit()

    flash("Faculty updated successfully!", "success")
    return redirect(url_for("admin.faculty_list"))
