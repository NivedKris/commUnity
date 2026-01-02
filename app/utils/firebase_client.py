import firebase_admin
from firebase_admin import credentials, auth
import os
from app.config import Config

# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                          Config.FIREBASE_ADMIN_SDK_PATH)

try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Firebase Admin SDK: {e}")

def verify_firebase_token(id_token):
    """Verify Firebase ID token and return decoded token"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        return None

def get_user_by_uid(uid):
    """Get Firebase user by UID"""
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        print(f"Error getting Firebase user: {e}")
        return None
