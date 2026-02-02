from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import SubjectType, Section, Edition ,Classification
from app.extensions import db
from app.models.student import StudentCourse
from app.utils.decorators import role_required

from . import admin_bp

@admin_bp.route("/settings")
@role_required("Admin")
def settings():
    Sections = Section.query.order_by(Section.name.asc()).all()
    SubjectTypes = SubjectType.query.order_by(SubjectType.name.asc()).all()
    Editions = Edition.query.order_by(Edition.name.asc()).all()
    StudentCourses = StudentCourse.query.order_by(StudentCourse.name.asc()).all()
    Classifications = Classification.query.order_by(Classification.name.asc()).all()
    return render_template("admin/settings.html",
                           sections=Sections,
                           subject_types=SubjectTypes,
                           editions=Editions,
                           student_courses=StudentCourses,
                           classifications=Classifications)


@admin_bp.route("/settings/add_section", methods=["POST"])
@role_required("Admin")
def add_section():
    name = request.form.get("name").capitalize()
    if not name:
        flash("Section name is required.", "error")
        return redirect(url_for("admin.settings"))

    if Section.query.filter_by(name=name).first():
        flash("Section already exists.", "error")
        return redirect(url_for("admin.settings"))
    
    new_section = Section(name=name)
    db.session.add(new_section)
    db.session.commit()
    flash("Section added successfully.", "success")
    return redirect(url_for("admin.settings"))


@admin_bp.route("/settings/add_subject_type", methods=["POST"])
@role_required("Admin")
def add_subject_type():
    name = request.form.get("name").capitalize()
    if not name:
        flash("Subject Type name is required.", "error")
        return redirect(url_for("admin.settings"))

    if SubjectType.query.filter_by(name=name).first():
        flash("Subject Type already exists.", "error")
        return redirect(url_for("admin.settings"))

    new_subject_type = SubjectType(name=name)
    db.session.add(new_subject_type)
    db.session.commit()
    flash("Subject Type added successfully.", "success")
    return redirect(url_for("admin.settings"))



@admin_bp.route("/settings/add_edition", methods=["POST"])
@role_required("Admin")
def add_edition():
    name = request.form.get("name").capitalize()
    if not name:
        flash("Edition name is required.", "error")
        return redirect(url_for("admin.settings"))
    if Edition.query.filter_by(name=name).first():
        flash("Edition already exists.", "error")
        return redirect(url_for("admin.settings"))
    
    new_edition = Edition(name=name)
    db.session.add(new_edition)
    db.session.commit()
    flash("Edition added successfully.", "success")
    return redirect(url_for("admin.settings"))



@admin_bp.route("/settings/add_student_course", methods=["POST"])
@role_required("Admin")
def add_student_course():
    name = request.form.get("name").capitalize()
    abbreviation = request.form.get("abbreviation").upper()
    if not name:
        flash("Course name is required.", "error")
        return redirect(url_for("admin.settings"))
    if StudentCourse.query.filter_by(name=name).first():
        flash("Course already exists.", "error")
        return redirect(url_for("admin.settings"))
    new_course = StudentCourse(abbreviation=abbreviation, name=name)
    db.session.add(new_course)
    db.session.commit()
    flash("Course added successfully.", "success")
    return redirect(url_for("admin.settings"))


@admin_bp.route("/settings/add_classification", methods=["POST"])
@role_required("Admin")
def add_classification():
    name=request.form.get("name").capitalize()
    if not name:
        flash("Classification name is required.", "error")
        return redirect(url_for("admin.settings"))
    if Classification.query.filter_by(name=name).first():
        flash("Classification already exists.", "error")
        return redirect(url_for("admin.settings"))
    new_classification = Classification(name=name)
    db.session.add(new_classification)
    db.session.commit()
    flash("Classification added successfully.", "success")
    return redirect(url_for("admin.settings"))
    