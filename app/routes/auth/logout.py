from flask import Blueprint, flash, request, render_template, redirect, session, url_for
from app.services.auth_services import authenticate_staff
from app.routes.auth import auth_bp


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.staff_login'))