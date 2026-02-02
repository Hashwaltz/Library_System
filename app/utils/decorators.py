from functools import wraps
from flask import session, abort, redirect, flash

def role_required(*allowed_roles):
    """
    Restrict access to users with specified roles.
    Usage:
        @role_required('Admin')
        @role_required('Librarian')
        @role_required('Admin', 'Librarian')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = session.get("role")
            if "user_id" not in session:
                flash("Please log in to access this page.", "error")
                return redirect("/staff_login")
            if not role or role not in allowed_roles:
                flash("You do not have permission to access this page.", "warning")
                return redirect("/staff_login")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
