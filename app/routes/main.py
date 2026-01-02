from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def landing():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')

@bp.route('/dashboard')
def dashboard():
    """Dashboard - requires authentication"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('dashboard/home.html')
