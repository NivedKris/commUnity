from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

bp = Blueprint('issues', __name__, url_prefix='/issues')

@bp.route('/')
@login_required
def list_issues():
    """List all user's reported issues"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # TODO: Fetch user's issues from database
    return render_template('issues/list.html')

@bp.route('/report')
@login_required
def report_issue():
    """Report new issue form"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return render_template('issues/report.html')

@bp.route('/submit', methods=['POST'])
@login_required
def submit_issue():
    """Handle issue submission"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # TODO: Save issue to database
    # Get form data
    # category = request.form.get('category')
    # location = request.form.get('location')
    # description = request.form.get('description')
    # priority = request.form.get('priority', 'low')
    # phone = request.form.get('phone')
    # anonymous = request.form.get('anonymous') == 'on'
    # photo = request.files.get('photo')
    
    return jsonify({'success': True, 'message': 'Issue reported successfully'})
