from flask import Blueprint, render_template
from datetime import datetime

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def landing():
    return render_template('public/landing.html', now=datetime.now())


@public_bp.route('/started')
def getting_started():
    return render_template('public/started.html')