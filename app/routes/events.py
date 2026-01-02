from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import current_user, login_required
from app.models import Event, User
from app.utils.supabase_client import supabase
from app.utils.storage_helper import upload_to_storage, delete_from_storage
from datetime import datetime
import uuid

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('/')
@login_required
def list_events():
    """List all events"""
    # Get filter parameters
    category = request.args.get('category')
    search = request.args.get('search')
    
    # Build filters
    filters = {}
    if category:
        filters['category'] = category
    
    # Fetch events from database
    events = Event.get_all(filters=filters, limit=50)
    
    # Search filter (client-side for now, can move to DB later)
    if search:
        search_lower = search.lower()
        events = [e for e in events if search_lower in e.title.lower() or search_lower in e.description.lower()]
    
    # Get attendee counts for each event
    events_with_counts = []
    for event in events:
        event_dict = {
            'id': str(event.id),
            'title': event.title,
            'description': event.description,
            'category': event.category,
            'date_time': event.date_time,
            'location': event.location,
            'image_url': event.image_url,
            'attendee_count': event.get_attendee_count()
        }
        events_with_counts.append(event_dict)
    
    return render_template('events/discover.html', events=events_with_counts, selected_category=category)

@bp.route('/my-events')
@login_required
def my_events():
    """List events user is attending or interested in"""
    try:
        # Get events created by user (organized events)
        organized_response = supabase.table('events')\
            .select('*')\
            .eq('organizer_id', current_user.id)\
            .order('date_time', desc=False)\
            .execute()
        
        organized_events = []
        if organized_response.data:
            for event_data in organized_response.data:
                event = Event(**event_data)
                organized_events.append({
                    'id': str(event.id),
                    'title': event.title,
                    'description': event.description,
                    'category': event.category,
                    'date_time': event.date_time,
                    'location': event.location,
                    'image_url': event.image_url,
                    'attendee_count': event.get_attendee_count()
                })
        
        # Get all RSVPs for current user
        rsvp_response = supabase.table('event_rsvps')\
            .select('event_id, status')\
            .eq('user_id', current_user.id)\
            .execute()
        
        # Separate events by status
        going_event_ids = []
        interested_event_ids = []
        
        if rsvp_response.data:
            going_event_ids = [r['event_id'] for r in rsvp_response.data if r['status'] == 'going']
            interested_event_ids = [r['event_id'] for r in rsvp_response.data if r['status'] == 'interested']
        
        # Get saved events
        saved_response = supabase.table('saved_events')\
            .select('event_id')\
            .eq('user_id', current_user.id)\
            .execute()
        
        saved_event_ids = [s['event_id'] for s in saved_response.data] if saved_response.data else []
        
        # Fetch event details
        going_events = []
        for event_id in going_event_ids:
            event = Event.get_by_id(event_id)
            if event:
                going_events.append({
                    'id': str(event.id),
                    'title': event.title,
                    'description': event.description,
                    'category': event.category,
                    'date_time': event.date_time,
                    'location': event.location,
                    'image_url': event.image_url,
                    'attendee_count': event.get_attendee_count()
                })
        
        interested_events = []
        for event_id in interested_event_ids:
            event = Event.get_by_id(event_id)
            if event:
                interested_events.append({
                    'id': str(event.id),
                    'title': event.title,
                    'description': event.description,
                    'category': event.category,
                    'date_time': event.date_time,
                    'location': event.location,
                    'image_url': event.image_url,
                    'attendee_count': event.get_attendee_count()
                })
        
        saved_events = []
        for event_id in saved_event_ids:
            event = Event.get_by_id(event_id)
            if event:
                saved_events.append({
                    'id': str(event.id),
                    'title': event.title,
                    'description': event.description,
                    'category': event.category,
                    'date_time': event.date_time,
                    'location': event.location,
                    'image_url': event.image_url,
                    'attendee_count': event.get_attendee_count()
                })
        
        return render_template('events/my_events.html', 
                             organized_events=organized_events,
                             going_events=going_events, 
                             interested_events=interested_events,
                             saved_events=saved_events)
    except Exception as e:
        print(f"Error fetching my events: {e}")
        import traceback
        traceback.print_exc()
        return render_template('events/my_events.html', organized_events=[], going_events=[], interested_events=[], saved_events=[])

@bp.route('/create', methods=['GET'])
@login_required
def create_event_form():
    """Show create event form"""
    return render_template('events/create.html')

@bp.route('/create', methods=['POST'])
@login_required
def create_event():
    """Handle event creation"""
    try:
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        date_time = request.form.get('date_time')
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        max_participants = request.form.get('max_participants')
        
        # Validate required fields
        if not all([title, description, category, date_time, location]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('events.create_event_form'))
        
        # Handle image upload
        image_url = None
        print(f"DEBUG: request.files = {request.files}")
        if 'image' in request.files:
            file = request.files['image']
            print(f"DEBUG: file = {file}, filename = {file.filename if file else 'None'}")
            if file and file.filename:
                print(f"DEBUG: Uploading to storage, bucket='events', folder='{current_user.id}'")
                image_url = upload_to_storage(file, 'events', folder=str(current_user.id))
                print(f"DEBUG: Image uploaded successfully: {image_url}")
            else:
                print("DEBUG: No file selected or empty filename")
        else:
            print("DEBUG: No image in request.files")
        
        # Convert date_time string to ISO format
        # Expected format: YYYY-MM-DDTHH:MM
        if date_time:
            dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            date_time = dt.isoformat()
        
        # Create event
        print(f"DEBUG: Creating event with image_url: {image_url}")
        event = Event.create(
            organizer_id=current_user.id,
            title=title,
            description=description,
            category=category,
            date_time=date_time,
            location=location,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            max_participants=int(max_participants) if max_participants else None,
            image_url=image_url
        )
        
        if event:
            print(f"DEBUG: Event created successfully!")
            print(f"DEBUG: Event ID: {event.id}")
            print(f"DEBUG: Event image_url: {event.image_url}")
            print(f"DEBUG: Event title: {event.title}")
            flash('Event created successfully!', 'success')
            return redirect(url_for('events.event_detail', event_id=event.id))
        else:
            flash('Failed to create event', 'error')
            return redirect(url_for('events.create_event_form'))
            
    except Exception as e:
        print(f"Error creating event: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while creating the event', 'error')
        return redirect(url_for('events.create_event_form'))

@bp.route('/<event_id>')
@login_required
def event_detail(event_id):
    """Event detail page"""
    event = Event.get_by_id(event_id)
    
    if not event:
        return "Event not found", 404
    
    # Get organizer info
    organizer = User.get_by_id(event.organizer_id)
    
    # Get attendees
    attendees_data = event.get_attendees()
    attendees = []
    for attendee_data in attendees_data[:10]:  # Show first 10
        user = User.get_by_id(attendee_data['user_id'])
        if user:
            attendees.append({
                'id': user.id,
                'name': user.name,
                'profile_picture': user.profile_picture
            })
    
    # Check if current user has RSVP'd
    user_rsvp = None
    try:
        rsvp_response = supabase.table('event_rsvps')\
            .select('status')\
            .eq('event_id', event_id)\
            .eq('user_id', current_user.id)\
            .execute()
        if rsvp_response.data and len(rsvp_response.data) > 0:
            user_rsvp = rsvp_response.data[0]['status']
    except Exception as e:
        print(f"Error checking RSVP: {e}")
    
    # Get comments
    comments = []
    try:
        comments_response = supabase.table('event_comments')\
            .select('*')\
            .eq('event_id', event_id)\
            .order('created_at', desc=True)\
            .limit(20)\
            .execute()
        
        if comments_response.data:
            for comment_data in comments_response.data:
                user = User.get_by_id(comment_data['user_id'])
                if user:
                    from datetime import datetime
                    created_at = datetime.fromisoformat(comment_data['created_at'].replace('Z', '+00:00'))
                    comments.append({
                        'id': comment_data['id'],
                        'content': comment_data['content'],
                        'user_name': user.name,
                        'user_picture': user.profile_picture,
                        'created_at': created_at
                    })
    except Exception as e:
        print(f"Error fetching comments: {e}")
    
    # Get similar events (same category, not this event)
    similar_events = []
    try:
        all_events = Event.get_all(filters={'category': event.category}, limit=10)
        for similar_event in all_events:
            if str(similar_event.id) != str(event_id):
                similar_events.append({
                    'id': str(similar_event.id),
                    'title': similar_event.title,
                    'date_time': similar_event.date_time,
                    'image_url': similar_event.image_url
                })
                if len(similar_events) >= 3:
                    break
    except Exception as e:
        print(f"Error fetching similar events: {e}")
    
    event_data = {
        'id': str(event.id),
        'title': event.title,
        'description': event.description,
        'category': event.category,
        'date_time': event.date_time,
        'location': event.location,
        'latitude': event.latitude,
        'longitude': event.longitude,
        'max_participants': event.max_participants,
        'image_url': event.image_url,
        'organizer_id': event.organizer_id,  # Add organizer_id for comparison
        'organizer': {
            'id': organizer.id,
            'name': organizer.name,
            'profile_picture': organizer.profile_picture
        } if organizer else None,
        'attendee_count': event.get_attendee_count(),
        'attendees': attendees,
        'user_rsvp': user_rsvp,
        'comments': comments,
        'similar_events': similar_events
    }
    
    # Debug: Print IDs for comparison
    print(f"Current user ID: {current_user.id} (type: {type(current_user.id)})")
    print(f"Event organizer ID: {event.organizer_id} (type: {type(event.organizer_id)})")
    print(f"Are they equal? {str(current_user.id) == str(event.organizer_id)}")
    
    return render_template('events/detail.html', event=event_data)

@bp.route('/api/<event_id>/rsvp', methods=['POST'])
@login_required
def rsvp_event(event_id):
    """RSVP to an event"""
    try:
        data = request.get_json()
        status = data.get('status', 'going')  # going, interested, not_going
        
        if status not in ['going', 'interested', 'not_going']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        # Check if event exists
        event = Event.get_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Check if already RSVP'd
        existing_rsvp = supabase.table('event_rsvps')\
            .select('id')\
            .eq('event_id', event_id)\
            .eq('user_id', current_user.id)\
            .execute()
        
        if existing_rsvp.data and len(existing_rsvp.data) > 0:
            # Update existing RSVP
            result = supabase.table('event_rsvps')\
                .update({'status': status})\
                .eq('event_id', event_id)\
                .eq('user_id', current_user.id)\
                .execute()
        else:
            # Create new RSVP
            rsvp_data = {
                'event_id': event_id,
                'user_id': current_user.id,
                'status': status
            }
            result = supabase.table('event_rsvps').insert(rsvp_data).execute()
            
            # Log activity
            if status == 'going':
                activity_data = {
                    'user_id': current_user.id,
                    'activity_type': 'event_rsvp',
                    'entity_type': 'event',
                    'entity_id': event_id,
                    'description': f'RSVPed to {event.title}'
                }
                supabase.table('user_activity').insert(activity_data).execute()
        
        if result.data:
            # Get updated attendee count
            attendee_count = event.get_attendee_count()
            return jsonify({
                'success': True,
                'status': status,
                'attendee_count': attendee_count
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to RSVP'}), 500
            
    except Exception as e:
        print(f"Error handling RSVP: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/<event_id>/comment', methods=['POST'])
@login_required
def post_comment(event_id):
    """Post a comment on an event"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'success': False, 'error': 'Comment cannot be empty'}), 400
        
        # Check if event exists
        event = Event.get_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Create comment
        comment_data = {
            'event_id': event_id,
            'user_id': current_user.id,
            'content': content
        }
        result = supabase.table('event_comments').insert(comment_data).execute()
        
        if result.data:
            return jsonify({
                'success': True,
                'comment': {
                    'id': result.data[0]['id'],
                    'content': content,
                    'user_name': current_user.name,
                    'user_picture': current_user.profile_picture,
                    'created_at': result.data[0]['created_at']
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to post comment'}), 500
            
    except Exception as e:
        print(f"Error posting comment: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/<event_id>/save', methods=['POST'])
@login_required
def save_event(event_id):
    """Save/unsave an event for later"""
    try:
        # Check if event exists
        event = Event.get_by_id(event_id)
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Check if already saved
        existing_save = supabase.table('saved_events')\
            .select('id')\
            .eq('event_id', event_id)\
            .eq('user_id', current_user.id)\
            .execute()
        
        if existing_save.data and len(existing_save.data) > 0:
            # Unsave - delete the record
            supabase.table('saved_events')\
                .delete()\
                .eq('event_id', event_id)\
                .eq('user_id', current_user.id)\
                .execute()
            
            return jsonify({
                'success': True,
                'saved': False
            })
        else:
            # Save - create new record
            save_data = {
                'event_id': event_id,
                'user_id': current_user.id
            }
            result = supabase.table('saved_events').insert(save_data).execute()
            
            if result.data:
                return jsonify({
                    'success': True,
                    'saved': True
                })
            else:
                return jsonify({'success': False, 'error': 'Failed to save event'}), 500
            
    except Exception as e:
        print(f"Error saving event: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/<event_id>/edit', methods=['GET'])
@login_required
def edit_event_form(event_id):
    """Show edit event form"""
    event = Event.get_by_id(event_id)
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('events.list_events'))
    
    # Only organizer can edit
    if str(event.organizer_id) != str(current_user.id):
        flash('You do not have permission to edit this event', 'error')
        return redirect(url_for('events.event_detail', event_id=event_id))
    
    return render_template('events/edit.html', event=event)

@bp.route('/<event_id>/edit', methods=['POST'])
@login_required
def edit_event(event_id):
    """Handle event update"""
    try:
        event = Event.get_by_id(event_id)
        
        if not event:
            flash('Event not found', 'error')
            return redirect(url_for('events.list_events'))
        
        # Only organizer can edit
        if str(event.organizer_id) != str(current_user.id):
            flash('You do not have permission to edit this event', 'error')
            return redirect(url_for('events.event_detail', event_id=event_id))
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        date_time = request.form.get('date_time')
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        max_participants = request.form.get('max_participants')
        
        # Validate required fields
        if not all([title, description, category, date_time, location]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('events.edit_event_form', event_id=event_id))
        
        # Handle image upload
        image_url = event.image_url  # Keep existing image
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Delete old image if exists
                if event.image_url:
                    delete_from_storage(event.image_url, 'events')
                image_url = upload_to_storage(file, 'events', folder=str(current_user.id))
        
        # Convert date_time string to ISO format
        if date_time:
            dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            date_time = dt.isoformat()
        
        # Update event in database
        update_data = {
            'title': title,
            'description': description,
            'category': category,
            'date_time': date_time,
            'location': location,
            'latitude': float(latitude) if latitude else None,
            'longitude': float(longitude) if longitude else None,
            'max_participants': int(max_participants) if max_participants else None,
            'image_url': image_url
        }
        
        result = supabase.table('events').update(update_data).eq('id', event_id).execute()
        
        if result.data:
            flash('Event updated successfully!', 'success')
            return redirect(url_for('events.event_detail', event_id=event_id))
        else:
            flash('Failed to update event', 'error')
            return redirect(url_for('events.edit_event_form', event_id=event_id))
            
    except Exception as e:
        print(f"Error updating event: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while updating the event', 'error')
        return redirect(url_for('events.edit_event_form', event_id=event_id))

@bp.route('/<event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete an event"""
    try:
        event = Event.get_by_id(event_id)
        
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Only organizer can delete
        if str(event.organizer_id) != str(current_user.id):
            return jsonify({'success': False, 'error': 'Permission denied'}), 403
        
        # Delete image from storage if exists
        if event.image_url:
            delete_from_storage(event.image_url, 'events')
        
        # Delete event from database (cascade will handle RSVPs, comments, etc.)
        result = supabase.table('events').delete().eq('id', event_id).execute()
        
        if result:
            flash('Event deleted successfully', 'success')
            return redirect(url_for('events.my_events'))
        else:
            flash('Failed to delete event', 'error')
            return redirect(url_for('events.event_detail', event_id=event_id))
            
    except Exception as e:
        print(f"Error deleting event: {e}")
        import traceback
        traceback.print_exc()
        flash('An error occurred while deleting the event', 'error')
        return redirect(url_for('events.event_detail', event_id=event_id))
