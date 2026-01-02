from supabase import create_client, Client
from app.config import Config

# Initialize Supabase client (anon key for user operations)
supabase: Client = None

# Initialize admin client (service role key for admin operations like storage)
supabase_admin: Client = None

try:
    # Create Supabase client - positional arguments only
    supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)
    print("✅ Supabase client initialized successfully")
    
    # Create admin client with service role key
    supabase_admin = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_ROLE_KEY)
    print("✅ Supabase admin client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Supabase client: {e}")
    import traceback
    traceback.print_exc()

def get_supabase_client():
    """Get Supabase client instance"""
    return supabase

def get_supabase_admin():
    """Get Supabase admin client instance (for storage, admin operations)"""
    return supabase_admin
