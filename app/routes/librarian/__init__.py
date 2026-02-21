from flask import Blueprint

librarian_bp = Blueprint("librarian", __name__)


from . import dashboard
