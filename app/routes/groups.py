from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_required
from app.models import Group, User
from app.utils.supabase_client import supabase
from app.utils.storage_helper import upload_to_storage, delete_from_storage

bp = Blueprint('groups', __name__, url_prefix='/groups')

@bp.route('/')
@login_required
def list_groups():
    """List all groups"""
    try:
        # Get filter parameters
        category = request.args.get('category')
        search = request.args.get('search')
        my_groups = request.args.get('my_groups') == 'true'
        
        # Build filters
        filters = {}
        if category:
            filters['category'] = category
        
        # Fetch groups
        if my_groups:
            # Get groups where user is a member
            member_response = supabase.table('group_members')\
                .select('group_id')\
                .eq('user_id', current_user.id)\
                .execute()
            
            if member_response.data:
                group_ids = [m['group_id'] for m in member_response.data]
                groups = []
                for group_id in group_ids:
                    group = Group.get_by_id(group_id)
                    if group:
                        groups.append(group)
            else:
                groups = []
        else:
            groups = Group.get_all(filters=filters)
        
        # Search filter
        if search and groups:
            search_lower = search.lower()
            groups = [g for g in groups if search_lower in g.name.lower() or search_lower in g.description.lower()]
        
        # Convert to dict with member counts
        groups_with_counts = []
        for group in groups:
            groups_with_counts.append({
                'id': str(group.id),
                'name': group.name,
                'description': group.description,
                'category': group.category,
                'image_url': group.image_url,
                'is_private': group.is_private,
                'member_count': group.get_member_count(),
                'is_member': group.is_member(current_user.id)
            })
        
        return render_template('groups/discover.html', groups=groups_with_counts, selected_category=category)
        
    except Exception as e:
        print(f"Error fetching groups: {e}")
        import traceback
        traceback.print_exc()
        return render_template('groups/discover.html', groups=[])

@bp.route('/<group_id>')
@login_required
def group_detail(group_id):
    """Group detail page"""
    try:
        group = Group.get_by_id(group_id)
        
        if not group:
            flash('Group not found', 'error')
            return redirect(url_for('groups.list_groups'))
        
        # Get creator info
        creator = User.get_by_id(group.creator_id)
        
        # Get members with user details
        members_data = group.get_members(limit=20)
        members = []
        for member_data in members_data:
            user = User.get_by_id(member_data['user_id'])
            if user:
                members.append({
                    'id': user.id,
                    'name': user.name,
                    'profile_picture': user.profile_picture,
                    'role': member_data['role'],
                    'joined_at': member_data['joined_at']
                })
        
        # Check if current user is a member
        is_member = group.is_member(current_user.id)
        user_role = group.get_user_role(current_user.id) if is_member else None
        
        # Get group posts (we'll implement this later when we add posts table)
        # For now, return empty posts
        posts = []
        
        group_data = {
            'id': str(group.id),
            'name': group.name,
            'description': group.description,
            'category': group.category,
            'image_url': group.image_url,
            'is_private': group.is_private,
            'created_at': group.created_at,
            'creator_id': group.creator_id,
            'creator': {
                'id': creator.id,
                'name': creator.name,
                'profile_picture': creator.profile_picture
            } if creator else None,
            'member_count': group.get_member_count(),
            'members': members,
            'is_member': is_member,
            'user_role': user_role,
            'posts': posts
        }
        
        return render_template('groups/detail.html', group=group_data)
        
    except Exception as e:
        print(f"Error fetching group detail: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred', 'error')
        return redirect(url_for('groups.list_groups'))

@bp.route('/create', methods=['GET'])
@login_required
def create_group_form():
    """Show create group form"""
    return render_template('groups/create.html')

@bp.route('/create', methods=['POST'])
@login_required
def create_group():
    """Handle group creation"""
    try:
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        is_private = request.form.get('is_private') == 'true'
        
        # Validate required fields
        if not all([name, description, category]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('groups.create_group_form'))
        
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url = upload_to_storage(file, 'groups', folder=str(current_user.id))
        
        # Create group
        group = Group.create(
            creator_id=current_user.id,
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            is_private=is_private
        )
        
        if group:
            flash('Group created successfully!', 'success')
            return redirect(url_for('groups.group_detail', group_id=group.id))
        else:
            flash('Failed to create group', 'error')
            return redirect(url_for('groups.create_group_form'))
            
    except Exception as e:
        print(f"Error creating group: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while creating the group', 'error')
        return redirect(url_for('groups.create_group_form'))

@bp.route('/<group_id>/edit', methods=['GET'])
@login_required
def edit_group_form(group_id):
    """Show edit group form"""
    group = Group.get_by_id(group_id)
    
    if not group:
        flash('Group not found', 'error')
        return redirect(url_for('groups.list_groups'))
    
    # Only creator or admin can edit
    user_role = group.get_user_role(current_user.id)
    if str(group.creator_id) != str(current_user.id) and user_role != 'admin':
        flash('You do not have permission to edit this group', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))
    
    group_data = {
        'id': str(group.id),
        'name': group.name,
        'description': group.description,
        'category': group.category,
        'image_url': group.image_url,
        'is_private': group.is_private
    }
    
    return render_template('groups/edit.html', group=group_data)

@bp.route('/<group_id>/edit', methods=['POST'])
@login_required
def edit_group(group_id):
    """Handle group update"""
    try:
        group = Group.get_by_id(group_id)
        
        if not group:
            flash('Group not found', 'error')
            return redirect(url_for('groups.list_groups'))
        
        # Only creator or admin can edit
        user_role = group.get_user_role(current_user.id)
        if str(group.creator_id) != str(current_user.id) and user_role != 'admin':
            flash('You do not have permission to edit this group', 'error')
            return redirect(url_for('groups.group_detail', group_id=group_id))
        
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        is_private = request.form.get('is_private') == 'true'
        delete_image = request.form.get('delete_image') == 'true'
        
        # Validate required fields
        if not all([name, description, category]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('groups.edit_group_form', group_id=group_id))
        
        # Handle image upload
        image_url = group.image_url  # Keep existing image
        
        if delete_image and group.image_url:
            delete_from_storage(group.image_url, 'groups')
            image_url = None
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Delete old image if exists
                if group.image_url:
                    delete_from_storage(group.image_url, 'groups')
                image_url = upload_to_storage(file, 'groups', folder=str(current_user.id))
        
        # Update group
        success = group.update(
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            is_private=is_private
        )
        
        if success:
            flash('Group updated successfully!', 'success')
            return redirect(url_for('groups.group_detail', group_id=group_id))
        else:
            flash('Failed to update group', 'error')
            return redirect(url_for('groups.edit_group_form', group_id=group_id))
            
    except Exception as e:
        print(f"Error updating group: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while updating the group', 'error')
        return redirect(url_for('groups.edit_group_form', group_id=group_id))

@bp.route('/<group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    """Delete a group"""
    try:
        group = Group.get_by_id(group_id)
        
        if not group:
            flash('Group not found', 'error')
            return redirect(url_for('groups.list_groups'))
        
        # Only creator can delete
        if str(group.creator_id) != str(current_user.id):
            flash('Only the group creator can delete this group', 'error')
            return redirect(url_for('groups.group_detail', group_id=group_id))
        
        # Delete image from storage if exists
        if group.image_url:
            delete_from_storage(group.image_url, 'groups')
        
        # Delete group (cascade will handle members)
        if group.delete():
            flash('Group deleted successfully', 'success')
            return redirect(url_for('groups.list_groups'))
        else:
            flash('Failed to delete group', 'error')
            return redirect(url_for('groups.group_detail', group_id=group_id))
            
    except Exception as e:
        print(f"Error deleting group: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while deleting the group', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))

@bp.route('/api/<group_id>/join', methods=['POST'])
@login_required
def join_group(group_id):
    """Join a group"""
    try:
        group = Group.get_by_id(group_id)
        
        if not group:
            return jsonify({'success': False, 'error': 'Group not found'}), 404
        
        # Check if already a member
        if group.is_member(current_user.id):
            return jsonify({'success': False, 'error': 'Already a member'}), 400
        
        # Add member
        if group.add_member(current_user.id):
            return jsonify({
                'success': True,
                'member_count': group.get_member_count()
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to join group'}), 500
            
    except Exception as e:
        print(f"Error joining group: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/<group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    """Leave a group"""
    try:
        group = Group.get_by_id(group_id)
        
        if not group:
            return jsonify({'success': False, 'error': 'Group not found'}), 404
        
        # Can't leave if you're the creator
        if str(group.creator_id) == str(current_user.id):
            return jsonify({'success': False, 'error': 'Creator cannot leave the group'}), 400
        
        # Check if member
        if not group.is_member(current_user.id):
            return jsonify({'success': False, 'error': 'Not a member'}), 400
        
        # Remove member
        if group.remove_member(current_user.id):
            return jsonify({
                'success': True,
                'member_count': group.get_member_count()
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to leave group'}), 500
            
    except Exception as e:
        print(f"Error leaving group: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
