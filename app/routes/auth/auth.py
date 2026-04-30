from flask import Blueprint, flash, request, render_template, redirect, session, url_for
from app.services.auth_services import authenticate_staff
from app.routes.auth import auth_bp
from datetime import datetime


@auth_bp.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user, error = authenticate_staff(email, password)

        if error:
            return render_template('auth/login.html', error=error)

        session["role"] = user.role
        session["username"] = user.username
        session["user_id"] = user.id


        if user.role == 'admin':
            print("Redirecting to admin dashboard...")
            return redirect(url_for('admin.dashboard'))

        elif user.role == 'Librarian':
            return redirect(url_for('librarian.dashboard'))

    return render_template('auth/login.html', 
                           error=error,
                           now=datetime.now())

