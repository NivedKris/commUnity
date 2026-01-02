"""Clean up test data from database"""
from app.utils.supabase_client import supabase
import sys

def clean_test_data(user_firebase_uid):
    """Remove test badges and activity that shouldn't exist"""
    try:
        # Get user ID
        user_result = supabase.table('users').select('id').eq('firebase_uid', user_firebase_uid).execute()
        if not user_result.data:
            print(f"User not found: {user_firebase_uid}")
            return
        
        user_id = user_result.data[0]['id']
        print(f"Found user ID: {user_id}")
        
        # Check what badges user has
        badges = supabase.table('user_badges').select('*').eq('user_id', user_id).execute()
        print(f"\nCurrent badges: {len(badges.data) if badges.data else 0}")
        for badge in badges.data or []:
            print(f"  - {badge['badge_type']} (earned: {badge['earned_at']})")
        
        # Keep only first_steps badge, remove others that weren't properly earned
        badges_to_keep = ['first_steps']
        for badge in badges.data or []:
            if badge['badge_type'] not in badges_to_keep:
                print(f"\n🗑️  Removing test badge: {badge['badge_type']}")
                supabase.table('user_badges').delete().eq('id', badge['id']).execute()
        
        # Check activity
        activities = supabase.table('user_activity').select('*').eq('user_id', user_id).execute()
        print(f"\nCurrent activities: {len(activities.data) if activities.data else 0}")
        for activity in activities.data or []:
            print(f"  - {activity['activity_type']}: {activity['description']}")
        
        print("\n✅ Cleanup complete!")
        
    except Exception as e:
        print(f"Error cleaning data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_test_data.py <firebase_uid>")
        print("Example: python clean_test_data.py your_firebase_uid_here")
        sys.exit(1)
    
    firebase_uid = sys.argv[1]
    clean_test_data(firebase_uid)
