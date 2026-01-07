from flask import Blueprint

librarian_bp = Blueprint("librarian", __name__)

# import routes after Blueprint is created
from . import dashboard
