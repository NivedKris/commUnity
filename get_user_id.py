"""Get current user ID from database"""
from app.utils.supabase_client import supabase
import sys

def get_user_id_by_email(email):
    """Get user ID by email"""
    try:
        result = supabase.table('users').select('id, name, email').eq('email', email).execute()
        if result.data and len(result.data) > 0:
            user = result.data[0]
            print(f"✅ Found user:")
            print(f"   ID: {user['id']}")
            print(f"   Name: {user['name']}")
            print(f"   Email: {user['email']}")
            return user['id']
        else:
            print(f"❌ No user found with email: {email}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run get_user_id.py <your_email>")
        sys.exit(1)
    
    email = sys.argv[1]
    get_user_id_by_email(email)
