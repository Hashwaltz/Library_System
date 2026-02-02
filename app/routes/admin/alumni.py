from app.models.student import StudentCourse, Student
from app.extensions import db
from app.utils.decorators import role_required
from flask import Blueprint, render_template, request, redirect, url_for, flash

from . import admin_bp


# -----------------------------
# ALUMNI LIST VIEW
# -----------------------------
@admin_bp.route("/alumni-list")
@role_required("Admin")
def alumni_list():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    students_pagination = Student.query.filter_by(status='ALUMNI')\
        .order_by(Student.lastname.asc())\
        .paginate(page=page, per_page=per_page)

    courses = StudentCourse.query.order_by(StudentCourse.name.asc()).all()

    return render_template(
        "admin/alumni_list.html",
        students_pagination=students_pagination,
        courses=courses
    )


# -----------------------------
# ADD ALUMNI
# -----------------------------
@admin_bp.route("/alumni/add", methods=["POST"])
@role_required("Admin")
def add_alumni():
    stdnum = request.form.get("stdnum").strip()
    firstname = request.form.get("firstname").strip()
    middlename = request.form.get("middlename").strip()
    lastname = request.form.get("lastname").strip()
    course_id = request.form.get("course_id")
    level = request.form.get("level")
    designation = request.form.get("designation").strip()
    contact = request.form.get("contact").strip()
    address = request.form.get("address").strip()
    email = request.form.get("email").strip()

    # Validation
    if not (stdnum and firstname and lastname and course_id and level and email):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("admin.alumni_list"))

    if not level.isdigit() or not (1 <= int(level) <= 4):
        flash("Level must be between 1 and 4.", "error")
        return redirect(url_for("admin.alumni_list"))

    if Student.query.filter_by(stdnum=stdnum).first():
        flash("Student number already exists.", "error")
        return redirect(url_for("admin.alumni_list"))

    if Student.query.filter_by(email=email).first():
        flash("Email already exists.", "error")
        return redirect(url_for("admin.alumni_list"))

    new_student = Student(
        stdnum=stdnum,
        lastname=lastname,
        firstname=firstname,
        middlename=middlename,
        email=email,
        level=level,
        designation=designation,
        course_id=course_id,
        address=address,
        phone=contact,
        status='ALUMNI'
    )

    db.session.add(new_student)
    db.session.commit()

    flash("Alumni added successfully!", "success")
    return redirect(url_for("admin.alumni_list"))


# -----------------------------
# EDIT ALUMNI
# -----------------------------
@admin_bp.route("/alumni/edit/<int:student_id>", methods=["POST"])
@role_required("Admin")
def edit_alumni(student_id):
    student = Student.query.get_or_404(student_id)

    stdnum = request.form.get("stdnum").strip()
    firstname = request.form.get("firstname").strip()
    middlename = request.form.get("middlename").strip()
    lastname = request.form.get("lastname").strip()
    course_id = request.form.get("course_id")
    level = request.form.get("level")
    designation = request.form.get("designation").strip()
    contact = request.form.get("contact").strip()
    address = request.form.get("address").strip()
    email = request.form.get("email").strip()

    # Validation
    if not (stdnum and firstname and lastname and course_id and level and email):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("admin.alumni_list"))

    if not level.isdigit() or not (1 <= int(level) <= 4):
        flash("Level must be between 1 and 4.", "error")
        return redirect(url_for("admin.alumni_list"))

    if Student.query.filter(Student.stdnum == stdnum, Student.id != student_id).first():
        flash("Student number already exists.", "error")
        return redirect(url_for("admin.alumni_list"))

    if Student.query.filter(Student.email == email, Student.id != student_id).first():
        flash("Email already exists.", "error")
        return redirect(url_for("admin.alumni_list"))

    student.stdnum = stdnum
    student.lastname = lastname
    student.firstname = firstname
    student.middlename = middlename
    student.email = email
    student.level = level
    student.designation = designation
    student.course_id = course_id
    student.address = address
    student.phone = contact
    student.status = 'ALUMNI'

    db.session.commit()

    flash("Alumni updated successfully!", "success")
    return redirect(url_for("admin.alumni_list"))
