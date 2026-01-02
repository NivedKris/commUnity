"""Helper functions for badge awarding system"""
from app.utils.supabase_client import supabase

# Badge definitions with their requirements
BADGE_REQUIREMENTS = {
    'first_steps': {
        'name': 'First Steps',
        'description': 'Joined the community',
        'check': lambda stats, user_id: True  # Auto-awarded on signup
    },
    'event_explorer': {
        'name': 'Event Explorer',
        'description': 'Attended 10 events',
        'check': lambda stats, user_id: stats.get('events_attended', 0) >= 10
    },
    'community_builder': {
        'name': 'Community Builder',
        'description': 'Joined 5 groups',
        'check': lambda stats, user_id: stats.get('groups_joined', 0) >= 5
    },
    'problem_solver': {
        'name': 'Problem Solver',
        'description': 'Reported 10 issues',
        'check': lambda stats, user_id: stats.get('issues_reported', 0) >= 10
    },
    'conversation_starter': {
        'name': 'Conversation Starter',
        'description': 'Posted 50 comments',
        'check': lambda stats, user_id: count_user_comments(user_id) >= 50
    },
    'super_star': {
        'name': 'Super Star',
        'description': 'Reached 1000 reputation points',
        'check': lambda stats, user_id: stats.get('reputation_points', 0) >= 1000
    },
    'event_host': {
        'name': 'Event Host',
        'description': 'Created an event',
        'check': lambda stats, user_id: has_created_event(user_id)
    },
    'group_creator': {
        'name': 'Group Creator',
        'description': 'Created a group',
        'check': lambda stats, user_id: has_created_group(user_id)
    },
    'helpful_neighbor': {
        'name': 'Helpful Neighbor',
        'description': 'Active in community discussions',
        'check': lambda stats, user_id: count_user_posts(user_id) >= 20
    }
}

def count_user_comments(user_id):
    """Count total comments by user across all tables"""
    try:
        # Count event comments
        event_comments = supabase.table('event_comments').select('id', count='exact').eq('user_id', user_id).execute()
        event_count = event_comments.count if hasattr(event_comments, 'count') else 0
        
        # Count group post comments
        group_comments = supabase.table('group_post_comments').select('id', count='exact').eq('user_id', user_id).execute()
        group_count = group_comments.count if hasattr(group_comments, 'count') else 0
        
        return event_count + group_count
    except Exception as e:
        print(f"Error counting comments: {e}")
        return 0

def count_user_posts(user_id):
    """Count total posts by user"""
    try:
        result = supabase.table('group_posts').select('id', count='exact').eq('user_id', user_id).execute()
        return result.count if hasattr(result, 'count') else 0
    except Exception as e:
        print(f"Error counting posts: {e}")
        return 0

def has_created_event(user_id):
    """Check if user has created any events"""
    try:
        result = supabase.table('events').select('id', count='exact').eq('organizer_id', user_id).execute()
        count = result.count if hasattr(result, 'count') else 0
        return count > 0
    except Exception as e:
        print(f"Error checking events: {e}")
        return False

def has_created_group(user_id):
    """Check if user has created any groups"""
    try:
        result = supabase.table('groups').select('id', count='exact').eq('creator_id', user_id).execute()
        count = result.count if hasattr(result, 'count') else 0
        return count > 0
    except Exception as e:
        print(f"Error checking groups: {e}")
        return False

def get_user_badges(user_id):
    """Get list of badge types already earned by user"""
    try:
        result = supabase.table('user_badges').select('badge_type').eq('user_id', user_id).execute()
        return [badge['badge_type'] for badge in result.data] if result.data else []
    except Exception as e:
        print(f"Error getting user badges: {e}")
        return []

def award_badge(user_id, badge_type):
    """Award a badge to a user"""
    try:
        # Check if badge already exists
        existing = supabase.table('user_badges').select('id').eq('user_id', user_id).eq('badge_type', badge_type).execute()
        
        if existing.data and len(existing.data) > 0:
            return False  # Badge already awarded
        
        # Insert new badge
        result = supabase.table('user_badges').insert({
            'user_id': user_id,
            'badge_type': badge_type
        }).execute()
        
        if result.data:
            print(f"✅ Awarded '{badge_type}' badge to user {user_id}")
            return True
        return False
        
    except Exception as e:
        print(f"Error awarding badge: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_and_award_badges(user_id):
    """
    Check user's achievements and award new badges
    Should be called after major actions (RSVP, join group, report issue, create event/group, post comment)
    """
    try:
        # Get user's current stats
        from app.models import User
        user = User.get_by_id(user_id)
        if not user:
            return []
        
        stats = user.get_stats()
        
        # Get badges already earned
        earned_badges = get_user_badges(user_id)
        
        # Check each badge requirement
        newly_awarded = []
        for badge_type, badge_info in BADGE_REQUIREMENTS.items():
            # Skip if already earned
            if badge_type in earned_badges:
                continue
            
            # Check if user meets requirements
            if badge_info['check'](stats, user_id):
                if award_badge(user_id, badge_type):
                    newly_awarded.append(badge_type)
        
        return newly_awarded
        
    except Exception as e:
        print(f"Error checking badges: {e}")
        import traceback
        traceback.print_exc()
        return []
