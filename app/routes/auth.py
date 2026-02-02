from flask import Blueprint, flash, request, jsonify, render_template, redirect, session, url_for
from app.models.user import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if not user or not check_password_hash(user.password_hash, request.form['password']):
            error = 'Invalid email or password'
        else:
            session["role"] = user.role
            session["username"] = user.username
            session["user_id"] = user.id
            if user.role == 'Admin':
                print("Redirecting to admin dashboard...")
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'Librarian':
                return redirect(url_for('librarian.dashboard'))
    return render_template('auth/login.html', error=error)




@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.staff_login'))
