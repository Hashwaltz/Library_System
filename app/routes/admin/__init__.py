from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from . import dashboard
from . import librarians
from . import books
from . import settings 
from . import students
from . import reports
from . import alumni
from . import faculty 
from . import audit_logs