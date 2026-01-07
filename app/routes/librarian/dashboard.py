from flask import Blueprint, render_template
from app.utils.decorators import role_required

from . import librarian_bp


@librarian_bp.route("/librarian/dashboard")
@role_required("librarian")
def dashboard():
    return render_template("librarian/dashboard.html")
