from app.models.entry_log import EntryLog
from app.models.student import Student
from app.models.borrowers import Borrower

from app.extensions import db
from app.utils.decorators import role_required
from flask import Blueprint, render_template, request
from . import admin_bp