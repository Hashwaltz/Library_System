# routes/entry.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models import EntryLog, Student
from datetime import datetime

from . import logs_bp 

@logs_bp.route("/entry-log", methods=["GET", "POST"])
def entry_log():
    now = datetime.now()
    students = Student.query.order_by(Student.lastname).all()
    
    if request.method == "POST":
        # Check if it's JSON request from QR/manual
        if request.is_json:
            data = request.get_json()
            stdnum = data.get("student_number")
            student = Student.query.filter_by(stdnum=stdnum).first()
            if student:
                course_name = student.course_rel[0].name if student.course_rel else ""
                return jsonify({
                    "status": "ok",
                    "name": f"{student.lastname}, {student.firstname}",
                    "course": course_name
                })
            return jsonify({"status": "error"})
        
        # Normal POST from form submission
        student_id = request.form.get("student_number")  # or student_id if using dropdown
        reason = request.form.get("reason") or request.form.get("other_reason")
        student = Student.query.filter_by(stdnum=student_id).first()
        if student:
            log = EntryLog(student_id=student.id, reason=reason, created_at=datetime.now())
            db.session.add(log)
            db.session.commit()
            flash("Entry successfully logged!", "success")
        else:
            flash("Student not found!", "error")
        return redirect(request.url)
    
    return render_template("logs/logging.html", students=students, now=now)