from flask_login import UserMixin
from app.utils.supabase_client import supabase
from datetime import datetime
import uuid

class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, id, email, name, profile_picture=None, location=None, 
                 interests=None, reputation_points=0, user_type='citizen', 
                 verified=False, phone_number=None, bio=None, cover_photo=None):
        self.id = id
        self.email = email
        self.name = name
        self.display_name = name  # Alias for templates
        self.profile_picture = profile_picture
        self.location = location
        self.interests = interests or []
        self.reputation_points = reputation_points
        self.user_type = user_type
        self.verified = verified
        self.phone_number = phone_number
        self.bio = bio
        self.cover_photo = cover_photo
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID from Supabase"""
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data.get('email'),
                    name=user_data.get('name'),
                    profile_picture=user_data.get('profile_picture'),
                    location=user_data.get('location'),
                    interests=user_data.get('interests'),
                    reputation_points=user_data.get('reputation_points', 0),
                    user_type=user_data.get('user_type', 'citizen'),
                    verified=user_data.get('verified', False),
                    phone_number=user_data.get('phone_number'),
                    bio=user_data.get('bio'),
                    cover_photo=user_data.get('cover_photo')
                )
            return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email from Supabase"""
        try:
            response = supabase.table('users').select('*').eq('email', email).execute()
            if response.data and len(response.data) > 0:
                user_data = response.data[0]
                return User(
                    id=user_data['id'],
                    email=user_data.get('email'),
                    name=user_data.get('name'),
                    profile_picture=user_data.get('profile_picture'),
                    location=user_data.get('location'),
                    interests=user_data.get('interests'),
                    reputation_points=user_data.get('reputation_points', 0),
                    user_type=user_data.get('user_type', 'citizen'),
                    verified=user_data.get('verified', False),
                    phone_number=user_data.get('phone_number'),
                    bio=user_data.get('bio'),
                    cover_photo=user_data.get('cover_photo')
                )
            return None
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None
    
    @staticmethod
    def create(firebase_uid, email, name, phone_number=None, user_type='citizen', 
               location=None, interests=None, bio=None):
        """Create new user in Supabase"""
        try:
            user_data = {
                'id': firebase_uid,
                'email': email,
                'name': name,
                'phone_number': phone_number,
                'user_type': user_type,
                'location': location,
                'interests': interests or [],
                'bio': bio,
                'reputation_points': 0,
                'verified': False,
                'created_at': datetime.utcnow().isoformat()
            }
            response = supabase.table('users').insert(user_data).execute()
            if response.data:
                # Create activity log entry
                activity_data = {
                    'user_id': firebase_uid,
                    'activity_type': 'joined',
                    'description': f'{name} joined the community',
                    'created_at': datetime.utcnow().isoformat()
                }
                supabase.table('user_activity').insert(activity_data).execute()
                
                # Award first badge
                badge_data = {
                    'user_id': firebase_uid,
                    'badge_type': 'first_steps',
                    'earned_at': datetime.utcnow().isoformat()
                }
                supabase.table('user_badges').insert(badge_data).execute()
                
                return User.get_by_id(firebase_uid)
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update(self, **kwargs):
        """Update user data"""
        try:
            response = supabase.table('users').update(kwargs).eq('id', self.id).execute()
            if response.data:
                # Update instance attributes
                for key, value in kwargs.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                return True
            return False
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def get_stats(self):
        """Get user statistics"""
        try:
            # Count events attended (RSVPs)
            events_response = supabase.table('event_rsvps')\
                .select('id', count='exact')\
                .eq('user_id', self.id)\
                .eq('status', 'going')\
                .execute()
            events_count = events_response.count or 0
            
            # Count groups joined
            groups_response = supabase.table('group_members')\
                .select('id', count='exact')\
                .eq('user_id', self.id)\
                .execute()
            groups_count = groups_response.count or 0
            
            # Count issues reported
            issues_response = supabase.table('issues')\
                .select('id', count='exact')\
                .eq('reporter_id', self.id)\
                .execute()
            issues_count = issues_response.count or 0
            
            return {
                'events_attended': events_count,
                'groups_joined': groups_count,
                'issues_reported': issues_count,
                'reputation_points': self.reputation_points
            }
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                'events_attended': 0,
                'groups_joined': 0,
                'issues_reported': 0,
                'reputation_points': self.reputation_points
            }
    
    def get_badges(self):
        """Get user's earned badges"""
        try:
            response = supabase.table('user_badges')\
                .select('*')\
                .eq('user_id', self.id)\
                .order('earned_at', desc=True)\
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching badges: {e}")
            return []
    
    def get_activity(self, limit=10):
        """Get user's recent activity"""
        try:
            response = supabase.table('user_activity')\
                .select('*')\
                .eq('user_id', self.id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching activity: {e}")
            return []


class Event:
    """Event model"""
    
    def __init__(self, id, organizer_id, title, description, category, 
                 date_time, location, latitude=None, longitude=None, 
                 max_participants=None, image_url=None, created_at=None, 
                 updated_at=None):
        self.id = id
        self.organizer_id = organizer_id
        self.title = title
        self.description = description
        self.category = category
        # Convert date_time string to datetime object if it's a string
        if isinstance(date_time, str):
            try:
                self.date_time = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
            except:
                self.date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        else:
            self.date_time = date_time
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.max_participants = max_participants
        self.image_url = image_url
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(organizer_id, title, description, category, date_time, 
               location, latitude=None, longitude=None, max_participants=None, 
               image_url=None):
        """Create new event"""
        try:
            event_data = {
                'organizer_id': organizer_id,
                'title': title,
                'description': description,
                'category': category,
                'date_time': date_time,
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'max_participants': max_participants,
                'image_url': image_url
            }
            response = supabase.table('events').insert(event_data).execute()
            if response.data:
                event_id = response.data[0]['id']
                
                # TODO: Log activity when we add 'event_created' to allowed activity types
                # For now, skip activity logging
                
                return Event.get_by_id(event_id)
            return None
        except Exception as e:
            print(f"Error creating event: {e}")
            return None
    
    @staticmethod
    def get_by_id(event_id):
        """Get event by ID"""
        try:
            response = supabase.table('events').select('*').eq('id', event_id).execute()
            if response.data and len(response.data) > 0:
                data = response.data[0]
                return Event(**data)
            return None
        except Exception as e:
            print(f"Error fetching event: {e}")
            return None
    
    @staticmethod
    def get_all(filters=None, limit=50):
        """Get all events with optional filters"""
        try:
            query = supabase.table('events').select('*')
            
            if filters:
                if 'category' in filters:
                    query = query.eq('category', filters['category'])
                if 'organizer_id' in filters:
                    query = query.eq('organizer_id', filters['organizer_id'])
            
            query = query.order('date_time', desc=False).limit(limit)
            response = query.execute()
            
            return [Event(**data) for data in response.data] if response.data else []
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []
    
    def get_attendees(self):
        """Get list of attendees"""
        try:
            response = supabase.table('event_rsvps')\
                .select('user_id, status, created_at')\
                .eq('event_id', self.id)\
                .eq('status', 'going')\
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching attendees: {e}")
            return []
    
    def get_attendee_count(self):
        """Get count of attendees"""
        try:
            response = supabase.table('event_rsvps')\
                .select('*', count='exact')\
                .eq('event_id', str(self.id))\
                .eq('status', 'going')\
                .execute()
            
            if hasattr(response, 'count') and response.count is not None:
                return response.count
            elif response.data:
                return len(response.data)
            return 0
        except Exception as e:
            print(f"Error counting attendees: {e}")
            import traceback
            traceback.print_exc()
            return 0


class Group:
    """Group model"""
    
    def __init__(self, id, creator_id, name, description, category, 
                 image_url=None, is_private=False, created_at=None, updated_at=None):
        self.id = id
        self.creator_id = creator_id
        self.name = name
        self.description = description
        self.category = category
        self.image_url = image_url
        self.is_private = is_private
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(creator_id, name, description, category, image_url=None, is_private=False):
        """Create new group"""
        try:
            group_data = {
                'creator_id': creator_id,
                'name': name,
                'description': description,
                'category': category,
                'image_url': image_url,
                'is_private': is_private
            }
            response = supabase.table('groups').insert(group_data).execute()
            if response.data:
                group_id = response.data[0]['id']
                
                # Add creator as admin member
                member_data = {
                    'group_id': group_id,
                    'user_id': creator_id,
                    'role': 'admin'
                }
                supabase.table('group_members').insert(member_data).execute()
                
                # TODO: Log activity when we add 'group_created' to allowed activity types
                # For now, skip activity logging
                
                return Group.get_by_id(group_id)
            return None
        except Exception as e:
            print(f"Error creating group: {e}")
            return None
    
    @staticmethod
    def get_by_id(group_id):
        """Get group by ID"""
        try:
            response = supabase.table('groups').select('*').eq('id', group_id).execute()
            if response.data and len(response.data) > 0:
                data = response.data[0]
                return Group(**data)
            return None
        except Exception as e:
            print(f"Error fetching group: {e}")
            return None
    
    @staticmethod
    def get_all(filters=None, limit=50):
        """Get all groups with optional filters"""
        try:
            query = supabase.table('groups').select('*')
            
            if filters:
                if 'category' in filters:
                    query = query.eq('category', filters['category'])
                if 'creator_id' in filters:
                    query = query.eq('creator_id', filters['creator_id'])
            
            query = query.order('created_at', desc=True).limit(limit)
            response = query.execute()
            
            return [Group(**data) for data in response.data] if response.data else []
        except Exception as e:
            print(f"Error fetching groups: {e}")
            return []
    
    def get_member_count(self):
        """Get count of members"""
        try:
            response = supabase.table('group_members')\
                .select('id', count='exact')\
                .eq('group_id', self.id)\
                .execute()
            return response.count or 0
        except Exception as e:
            print(f"Error counting members: {e}")
            return 0
    
    def get_members(self, limit=50):
        """Get group members with user details"""
        try:
            response = supabase.table('group_members')\
                .select('user_id, role, joined_at')\
                .eq('group_id', self.id)\
                .order('joined_at', desc=False)\
                .limit(limit)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching members: {e}")
            return []
    
    def is_member(self, user_id):
        """Check if user is a member"""
        try:
            response = supabase.table('group_members')\
                .select('id')\
                .eq('group_id', self.id)\
                .eq('user_id', user_id)\
                .execute()
            return len(response.data) > 0 if response.data else False
        except Exception as e:
            print(f"Error checking membership: {e}")
            return False
    
    def get_user_role(self, user_id):
        """Get user's role in group"""
        try:
            response = supabase.table('group_members')\
                .select('role')\
                .eq('group_id', self.id)\
                .eq('user_id', user_id)\
                .execute()
            return response.data[0]['role'] if response.data else None
        except Exception as e:
            print(f"Error fetching user role: {e}")
            return None
    
    def add_member(self, user_id, role='member'):
        """Add a member to the group"""
        try:
            member_data = {
                'group_id': self.id,
                'user_id': user_id,
                'role': role
            }
            response = supabase.table('group_members').insert(member_data).execute()
            return response.data is not None
        except Exception as e:
            print(f"Error adding member: {e}")
            return False
    
    def remove_member(self, user_id):
        """Remove a member from the group"""
        try:
            response = supabase.table('group_members')\
                .delete()\
                .eq('group_id', self.id)\
                .eq('user_id', user_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Error removing member: {e}")
            return False
    
    def update(self, **kwargs):
        """Update group details"""
        try:
            update_data = {}
            allowed_fields = ['name', 'description', 'category', 'image_url', 'is_private']
            
            for key, value in kwargs.items():
                if key in allowed_fields and value is not None:
                    update_data[key] = value
            
            if update_data:
                response = supabase.table('groups').update(update_data).eq('id', self.id).execute()
                return response.data is not None
            return False
        except Exception as e:
            print(f"Error updating group: {e}")
            return False
    
    def delete(self):
        """Delete group"""
        try:
            # Delete all members first
            supabase.table('group_members').delete().eq('group_id', self.id).execute()
            # Delete the group
            response = supabase.table('groups').delete().eq('id', self.id).execute()
            return True
        except Exception as e:
            print(f"Error deleting group: {e}")
            return False


class Issue:
    """Issue model"""
    
    def __init__(self, id, reporter_id, title, description, category, 
                 location, latitude=None, longitude=None, image_url=None,
                 status='open', priority='medium', created_at=None, updated_at=None):
        self.id = id
        self.reporter_id = reporter_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url
        self.status = status
        self.priority = priority
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(reporter_id, title, description, category, location, 
               latitude=None, longitude=None, image_url=None, priority='medium'):
        """Create new issue"""
        try:
            issue_data = {
                'reporter_id': reporter_id,
                'title': title,
                'description': description,
                'category': category,
                'location': location,
                'latitude': latitude,
                'longitude': longitude,
                'image_url': image_url,
                'priority': priority,
                'status': 'open'
            }
            response = supabase.table('issues').insert(issue_data).execute()
            if response.data:
                issue_id = response.data[0]['id']
                
                # Log activity
                activity_data = {
                    'user_id': reporter_id,
                    'activity_type': 'issue_reported',
                    'entity_type': 'issue',
                    'entity_id': issue_id,
                    'description': f'Reported issue: {title}'
                }
                supabase.table('user_activity').insert(activity_data).execute()
                
                return Issue.get_by_id(issue_id)
            return None
        except Exception as e:
            print(f"Error creating issue: {e}")
            return None
    
    @staticmethod
    def get_by_id(issue_id):
        """Get issue by ID"""
        try:
            response = supabase.table('issues').select('*').eq('id', issue_id).execute()
            if response.data and len(response.data) > 0:
                data = response.data[0]
                return Issue(**data)
            return None
        except Exception as e:
            print(f"Error fetching issue: {e}")
            return None
    
    @staticmethod
    def get_all(filters=None, limit=50):
        """Get all issues with optional filters"""
        try:
            query = supabase.table('issues').select('*')
            
            if filters:
                if 'status' in filters:
                    query = query.eq('status', filters['status'])
                if 'category' in filters:
                    query = query.eq('category', filters['category'])
                if 'reporter_id' in filters:
                    query = query.eq('reporter_id', filters['reporter_id'])
            
            query = query.order('created_at', desc=True).limit(limit)
            response = query.execute()
            
            return [Issue(**data) for data in response.data] if response.data else []
        except Exception as e:
            print(f"Error fetching issues: {e}")
            return []
    
    def update_status(self, new_status, user_id):
        """Update issue status"""
        try:
            # Update status
            response = supabase.table('issues')\
                .update({'status': new_status})\
                .eq('id', self.id)\
                .execute()
            
            if response.data:
                # Log status change
                update_data = {
                    'issue_id': self.id,
                    'user_id': user_id,
                    'content': f'Status changed from {self.status} to {new_status}',
                    'update_type': 'status_change',
                    'old_status': self.status,
                    'new_status': new_status
                }
                supabase.table('issue_updates').insert(update_data).execute()
                
                self.status = new_status
                return True
            return False
        except Exception as e:
            print(f"Error updating issue status: {e}")
            return False
