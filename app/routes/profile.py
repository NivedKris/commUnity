from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.utils.storage_helper import upload_to_storage, delete_from_storage
from app.utils.supabase_client import supabase
from app.models import User

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def view_profile():
    """View user's own profile"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # Get real user stats from database
    stats = current_user.get_stats()
    badges = current_user.get_badges()
    activity = current_user.get_activity(limit=10)
    
    return render_template('profile/view.html', 
                         stats=stats, 
                         badges=badges, 
                         activity=activity)

@bp.route('/<user_id>')
@login_required
def view_user_profile(user_id):
    """View another user's profile"""
    # If viewing own profile, redirect to main profile page
    if user_id == str(current_user.id):
        return redirect(url_for('profile.view_profile'))
    
    # Get user data
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    
    # Get user stats
    stats = user.get_stats()
    badges = user.get_badges()
    activity = user.get_activity(limit=10)
    
    return render_template('profile/view.html', 
                         user=user,
                         stats=stats, 
                         badges=badges, 
                         activity=activity,
                         is_own_profile=False)

@bp.route('/edit')
@login_required
def edit_profile():
    """Edit profile page"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return render_template('profile/edit.html')

@bp.route('/update', methods=['POST'])
@login_required
def update_profile():
    """Handle profile update"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        # Build update dict
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'bio' in data:
            update_data['bio'] = data['bio']
        if 'location' in data:
            update_data['location'] = data['location']
        if 'phone_number' in data:
            update_data['phone_number'] = data['phone_number']
        if 'interests' in data:
            update_data['interests'] = data['interests']
        
        # Update in database
        result = supabase.table('users').update(update_data).eq('id', current_user.id).execute()
        
        if result.data:
            # Update current_user object
            for key, value in update_data.items():
                if hasattr(current_user, key):
                    setattr(current_user, key, value)
            
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Database update failed'}), 500
            
    except Exception as e:
        print(f"Error updating profile: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    """Upload profile avatar"""
    try:
        if 'avatar' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Upload to Supabase Storage
        public_url = upload_to_storage(file, 'avatars', folder=str(current_user.id))
        
        if not public_url:
            return jsonify({'success': False, 'error': 'Upload failed'}), 500
        
        # Delete old avatar if exists
        if current_user.profile_picture:
            delete_from_storage(current_user.profile_picture, 'avatars')
        
        # Update user record in database
        result = supabase.table('users').update({
            'profile_picture': public_url
        }).eq('id', current_user.id).execute()
        
        if result.data:
            # Update current_user object
            current_user.profile_picture = public_url
            return jsonify({
                'success': True,
                'url': public_url,
                'message': 'Profile picture updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Database update failed'}), 500
            
    except Exception as e:
        print(f"Error uploading avatar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/upload-cover', methods=['POST'])
@login_required
def upload_cover():
    """Upload profile cover photo"""
    try:
        if 'cover' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['cover']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Upload to Supabase Storage
        public_url = upload_to_storage(file, 'covers', folder=str(current_user.id))
        
        if not public_url:
            return jsonify({'success': False, 'error': 'Upload failed'}), 500
        
        # Delete old cover if exists
        if current_user.cover_photo:
            delete_from_storage(current_user.cover_photo, 'covers')
        
        # Update user record in database
        result = supabase.table('users').update({
            'cover_photo': public_url
        }).eq('id', current_user.id).execute()
        
        if result.data:
            # Update current_user object
            current_user.cover_photo = public_url
            return jsonify({
                'success': True,
                'url': public_url,
                'message': 'Cover photo updated successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Database update failed'}), 500
            
    except Exception as e:
        print(f"Error uploading cover: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
