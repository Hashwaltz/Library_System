from flask import render_template, request
from app.extensions import db
from app.utils.decorators import role_required


from . import admin_bp


@role_required("admin")
@admin_bp.route()
def borrow_logs():
    return render_template("admin/logs.html")