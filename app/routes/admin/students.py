from app.models.student import StudentCourse, Student
from app.extensions import db
from app.utils.decorators import role_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.helpers import log_audit  # for auditing

from . import admin_bp


@admin_bp.route("/students-list")
@role_required("Admin")
def students_list():
    page = request.args.get("page", 1, type=int)
    per_page = 10  # number of students per page

    # Paginate students ordered by last_name
    students_pagination = Student.query.filter_by(status="ACTIVE").order_by(Student.lastname.asc()).paginate(page=page, per_page=per_page)
    courses = StudentCourse.query.order_by(StudentCourse.name.asc()).all()

    return render_template(
        "admin/students_list.html",
        students_pagination=students_pagination,
        courses=courses
    )


@admin_bp.route("/students/add", methods=["POST"])
@role_required("Admin")
def add_student():
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
    status = request.form.get("status", "ACTIVE")  # default to ACTIVE

    # Validation
    if not (stdnum and firstname and lastname and course_id and level and email):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("admin.students_list"))

    if not level.isdigit() or not (1 <= int(level) <= 4):
        flash("Level must be between 1 and 4.", "error")
        return redirect(url_for("admin.students_list"))

    if Student.query.filter_by(stdnum=stdnum).first():
        flash("Student number already exists.", "error")
        return redirect(url_for("admin.students_list"))

    if Student.query.filter_by(email=email).first():
        flash("Email already exists.", "error")
        return redirect(url_for("admin.students_list"))

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
        status=status
    )

    db.session.add(new_student)
    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="ADD STUDENT",
        table_name="student",
        record_id=new_student.id,
        new_data={
            "stdnum": new_student.stdnum,
            "firstname": new_student.firstname,
            "middlename": new_student.middlename,
            "lastname": new_student.lastname,
            "email": new_student.email,
            "level": new_student.level,
            "designation": new_student.designation,
            "course_id": new_student.course_id,
            "address": new_student.address,
            "phone": new_student.phone,
            "status": new_student.status
        }
    )

    flash("Student added successfully!", "success")
    return redirect(url_for("admin.students_list"))


@admin_bp.route("/students/edit/<int:student_id>", methods=["POST"])
@role_required("Admin")
def edit_student(student_id):
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
    status = request.form.get("status", "ACTIVE")

    # Validation
    if not (stdnum and firstname and lastname and course_id and level and email):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("admin.students_list"))

    if not level.isdigit() or not (1 <= int(level) <= 4):
        flash("Level must be between 1 and 4.", "error")
        return redirect(url_for("admin.students_list"))

    if Student.query.filter(Student.stdnum == stdnum, Student.id != student_id).first():
        flash("Student number already exists.", "error")
        return redirect(url_for("admin.students_list"))

    if Student.query.filter(Student.email == email, Student.id != student_id).first():
        flash("Email already exists.", "error")
        return redirect(url_for("admin.students_list"))

    # Save old data for audit
    old_data = {
        "stdnum": student.stdnum,
        "firstname": student.firstname,
        "middlename": student.middlename,
        "lastname": student.lastname,
        "email": student.email,
        "level": student.level,
        "designation": student.designation,
        "course_id": student.course_id,
        "address": student.address,
        "phone": student.phone,
        "status": student.status
    }

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
    student.status = status

    db.session.commit()

    # --- Audit log ---
    new_data = {
        "stdnum": student.stdnum,
        "firstname": student.firstname,
        "middlename": student.middlename,
        "lastname": student.lastname,
        "email": student.email,
        "level": student.level,
        "designation": student.designation,
        "course_id": student.course_id,
        "address": student.address,
        "phone": student.phone,
        "status": student.status
    }
    log_audit(
        action="EDIT STUDENT",
        table_name="student",
        record_id=student.id,
        old_data=old_data,
        new_data=new_data
    )

    flash("Student updated successfully!", "success")
    return redirect(url_for("admin.students_list"))
