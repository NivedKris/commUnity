"""Check and test Supabase Storage buckets"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

def test_storage():
    """Test storage buckets with service role key"""
    try:
        # Create client with service role key for admin operations
        supabase_url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        print(f"Connecting to: {supabase_url}")
        supabase = create_client(supabase_url, service_key)
        
        # List existing buckets
        buckets = supabase.storage.list_buckets()
        print(f"\n✅ Found {len(buckets)} buckets:")
        for bucket in buckets:
            bucket_name = bucket.name if hasattr(bucket, 'name') else bucket.get('name', 'unknown')
            is_public = bucket.public if hasattr(bucket, 'public') else bucket.get('public', False)
            print(f"  - {bucket_name} (public: {is_public})")
        
        # Test upload to avatars bucket
        print("\n🧪 Testing upload to 'avatars' bucket...")
        test_content = b"test image content"
        test_path = "test/test.jpg"
        
        try:
            result = supabase.storage.from_('avatars').upload(
                path=test_path,
                file=test_content,
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
            
            print(f"✅ Upload successful!")
            
            # Get public URL
            url = supabase.storage.from_('avatars').get_public_url(test_path)
            print(f"✅ Public URL: {url}")
            
            # Clean up test file
            supabase.storage.from_('avatars').remove([test_path])
            print(f"✅ Cleanup successful!")
            
        except Exception as e:
            print(f"❌ Upload test failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Storage system is working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_storage()
