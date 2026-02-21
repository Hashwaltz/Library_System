from flask import render_template, request, jsonify
from datetime import datetime, date, time
from app.extensions import db
from app.models import Student, EntryLog, Borrower, Guest
from sqlalchemy import func

from . import logs_bp



@logs_bp.route("/entry-log", methods=["GET", "POST"])
def entry_log():
    now = datetime.now()

    # ================= AUTO LOGOUT AT 7PM =================
    if now.time() >= time(19, 0):
        open_logs = EntryLog.query.filter_by(status="IN").all()
        for log in open_logs:
            auto_out = EntryLog(
                student_id=log.student_id if log.student_id else None,
                borrower_id=log.borrower_id if log.borrower_id else None,
                guest_id=log.guest_id if log.guest_id else None,
                reason="Auto OUT (7PM)",
                status="OUT"
            )
            db.session.add(auto_out)
        db.session.commit()

    if request.method == "POST":

        # ================= AJAX STUDENT LOOKUP =================
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
            return jsonify({"status": "error"})

        # ================= MANUAL / SCAN SUBMIT =================
        # Detect if it's a student or guest submission
        student_number = request.form.get("student_number", "").strip().upper()
        fullname = request.form.get("fullname", "").strip()
        designation = request.form.get("designation", "")
        reason = request.form.get("reason") or request.form.get("other_reason")

        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        # ---------- STUDENT LOG ----------
        if student_number:
            student = Student.query.filter(func.upper(Student.stdnum) == student_number).first()
            if not student:
                return jsonify({"status": "error", "message": "Student not found!"})

            last_log = EntryLog.query.filter(
                EntryLog.student_id == student.id,
                EntryLog.timestamp.between(today_start, today_end)
            ).order_by(EntryLog.timestamp.desc()).first()

            status = "IN" if not last_log or last_log.status == "OUT" else "OUT"
            new_log = EntryLog(student_id=student.id, reason=reason, status=status)
            db.session.add(new_log)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": f"Logged {status} successfully!",
                "mode": status
            })

        # ---------- GUEST / BORROWER LOG ----------
        elif fullname:
            # Check if designation indicates Borrower or Guest
            if designation.lower() in ["student", "borrower", "staff", "faculty"]:
                person = Borrower.query.filter(func.lower(Borrower.lastname + ' ' + Borrower.firstname) == fullname.lower()).first()
                if not person:
                    # Auto-create borrower if not exists
                    person = Borrower(
                        lastname=fullname.split()[-1],
                        firstname=" ".join(fullname.split()[:-1]) or fullname,
                        borrower_type=designation
                    )
                    db.session.add(person)
                    db.session.commit()
                last_log = EntryLog.query.filter(
                    EntryLog.borrower_id == person.id,
                    EntryLog.timestamp.between(today_start, today_end)
                ).order_by(EntryLog.timestamp.desc()).first()

                status = "IN" if not last_log or last_log.status == "OUT" else "OUT"
                new_log = EntryLog(borrower_id=person.id, reason=reason, status=status)
            else:
                # Guest
                person = Guest.query.filter(func.lower(Guest.fullname) == fullname.lower()).first()
                if not person:
                    person = Guest(fullname=fullname, designation=designation)
                    db.session.add(person)
                    db.session.commit()

                last_log = EntryLog.query.filter(
                    EntryLog.guest_id == person.id,
                    EntryLog.timestamp.between(today_start, today_end)
                ).order_by(EntryLog.timestamp.desc()).first()

                status = "IN" if not last_log or last_log.status == "OUT" else "OUT"
                new_log = EntryLog(guest_id=person.id, reason=reason, status=status)

            db.session.add(new_log)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": f"{designation} {status} logged successfully!",
                "mode": status
            })

        return jsonify({"status": "error", "message": "Invalid submission!"})

    return render_template("logs/logging.html", now=now)