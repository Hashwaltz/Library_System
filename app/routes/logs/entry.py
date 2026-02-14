from flask import render_template, request, jsonify
from datetime import datetime, date
from app.extensions import db
from app.models import Student, EntryLog
from sqlalchemy import func

from . import logs_bp

@logs_bp.route("/entry-log", methods=["GET", "POST"])
def entry_log():
    now = datetime.now()

    if request.method == "POST":

        # ================= AJAX REQUEST =================
        if request.is_json:
            data = request.get_json()
            stdnum = data.get("student_number", "").strip().upper()

            student = Student.query.filter(func.upper(Student.stdnum) == stdnum).first()

            if student:
                return jsonify({
                    "status": "ok",
                    "name": f"{student.lastname.upper()}, {student.firstname.upper()}",
                    "course": f"{student.course.name} - {student.level}" if student.course else ""
                })

            return jsonify({"status": "error", "message": "Student not found"})

        # ================= MANUAL SUBMISSION =================
        student_number = request.form.get("student_number", "").strip().upper()
        reason = request.form.get("reason") or request.form.get("other_reason")

        student = Student.query.filter(func.upper(Student.stdnum) == student_number).first()

        if not student:
            return jsonify({"status": "error", "message": "Student not found!"})

        # Check if there is already a log for today
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        existing_log = EntryLog.query.filter(
            EntryLog.student_id == student.id,
            EntryLog.timestamp.between(today_start, today_end)
        ).first()

        if existing_log:
            return jsonify({"status": "warning", "message": "This student has already logged an entry today!"})

        # Log the entry
        log = EntryLog(student_id=student.id, reason=reason)
        db.session.add(log)
        db.session.commit()

        return jsonify({"status": "success", "message": "Entry successfully logged!"})

    return render_template("logs/logging.html", now=now)
