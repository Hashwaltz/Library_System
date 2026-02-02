from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.utils.decorators import role_required
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.user import User
from app.utils.helpers import log_audit

from . import admin_bp




@admin_bp.route("/manage_librarians")
@role_required("Admin")
def manage_librarians():
    librarians = User.query.order_by(User.username.asc()).all()
    return render_template("admin/librarians.html", users=librarians)


@admin_bp.route("/add_librarian", methods=["POST"])
@role_required("Admin")
def add_librarian():
    username = request.form.get("username")
    email = request.form.get("email")
    role = request.form.get("role")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("All fields are required.", "error")
        return redirect(url_for("admin.manage_librarians"))
    
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        flash("Username or email already exists.", "error")
        return redirect(url_for("admin.manage_librarians"))
    
    new_librarian = User(
        username=username,
        email=email,
        role=role, 
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_librarian)
    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="ADD LIBRARIAN",
        table_name="user",
        record_id=new_librarian.id,
        new_data={
            "username": username,
            "email": email,
            "role": role,
            "is_active": new_librarian.is_active
        }
    )
    # -----------------

    flash("Librarian added successfully.", "success")
    return redirect(url_for("admin.manage_librarians"))


@admin_bp.route("/edit_librarian/<int:user_id>", methods=["POST"])
@role_required("Admin")
def edit_librarian(user_id):
    librarian = User.query.get_or_404(user_id)

    # Save old data for audit
    old_data = {
        "username": librarian.username,
        "email": librarian.email,
        "role": librarian.role,
        "is_active": librarian.is_active
    }

    username = request.form.get("username")
    email = request.form.get("email")
    role = request.form.get("role")
    is_active = request.form.get("is_active") 
    password = request.form.get("password")

    if not username or not email:
        flash("Username and email are required.", "error")
        return redirect(url_for("admin.manage_librarians"))

    librarian.username = username
    librarian.email = email
    librarian.role = role
    librarian.is_active = True if is_active == "true" else False

    if password:
        librarian.password_hash = generate_password_hash(password)

    db.session.commit()

    # --- Audit log ---
    log_audit(
        action="EDIT LIBRARIAN",
        table_name="user",
        record_id=librarian.id,
        old_data=old_data,
        new_data={
            "username": librarian.username,
            "email": librarian.email,
            "role": librarian.role,
            "is_active": librarian.is_active
        }
    )
    # -----------------

    flash("Librarian updated successfully.", "success")
    return redirect(url_for("admin.manage_librarians"))