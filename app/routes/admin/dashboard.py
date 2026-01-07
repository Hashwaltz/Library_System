from flask import Blueprint, render_template
from app.utils.decorators import role_required

from . import admin_bp


@admin_bp.route("/admin/dashboard")
@role_required("admin")
def dashboard():
    return render_template("admin/dashboard.html")
