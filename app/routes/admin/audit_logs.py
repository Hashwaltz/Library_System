from flask import render_template, request, jsonify
from app.models.audit_log import AuditLog
from app.extensions import db
from app.utils.decorators import role_required
from . import admin_bp

@admin_bp.route("/audit-logs")
@role_required("Admin")
def audit_logs():
    page = request.args.get("page", 1, type=int)
    per_page = 20

    logs_pagination = AuditLog.query\
        .order_by(AuditLog.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template("admin/audit_logs.html", logs_pagination=logs_pagination)


@admin_bp.route("/audit-log/<int:log_id>", endpoint="audit_log_detail")
@role_required("Admin")
def audit_log_detail(log_id):
    log = AuditLog.query.get_or_404(log_id)
    return jsonify({
        "Date & Time": log.timestamp.strftime("%Y-%m-%d %I:%M %p"),
        "Admin ID": log.user_id or "System",
        "Action": log.action,
        "Table": log.table_name,
        "Record ID": log.record_id or "-",
        "Old Data": log.old_data or "-",
        "New Data": log.new_data or "-"
    })
