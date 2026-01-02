from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app.utils.firebase_client import verify_firebase_token
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and handler"""
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return render_template('auth/signup.html')
    
    # Handle POST request (signup)
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        location = data.get('location')
        interests = data.get('interests', [])
        
        # Verify Firebase token
        decoded_token = verify_firebase_token(id_token)
        if not decoded_token:
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        firebase_uid = decoded_token['uid']
        
        # Check if user already exists
        existing_user = User.get_by_id(firebase_uid)
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user in Supabase with all signup data
        user = User.create(
            firebase_uid=firebase_uid,
            email=email,
            name=name,
            phone_number=phone,
            user_type='citizen',
            location=location,
            interests=interests if interests else []
        )
        
        # Log the user in
        login_user(user)
        
        return jsonify({'success': True, 'message': 'Account created successfully'}), 200
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify Firebase token and create session"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        # Verify Firebase token
        decoded_token = verify_firebase_token(id_token)
        if not decoded_token:
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        firebase_uid = decoded_token['uid']
        email = decoded_token.get('email')
        phone = decoded_token.get('phone_number')
        
        # Get or create user
        user = User.get_by_id(firebase_uid)
        
        if not user:
            # Create new user if doesn't exist (phone login case)
            user = User.create(
                firebase_uid=firebase_uid,
                email=email or '',
                name=phone or 'User',
                phone_number=phone,
                user_type='citizen'
            )
            
            if not user:
                return jsonify({'error': 'Failed to create user'}), 500
        
        # Log the user in
        login_user(user)
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"Token verification error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('main.landing'))
