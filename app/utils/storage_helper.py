"""Helper functions for Supabase Storage operations"""
import os
import uuid
from werkzeug.utils import secure_filename
from app.utils.supabase_client import supabase_admin

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_storage(file, bucket_name, folder=''):
    """
    Upload file to Supabase Storage
    
    Args:
        file: FileStorage object from Flask request
        bucket_name: Name of the storage bucket (avatars, covers, etc.)
        folder: Optional folder path within bucket
    
    Returns:
        Public URL of uploaded file or None on error
    """
    try:
        print(f"DEBUG [storage_helper]: Starting upload - bucket={bucket_name}, folder={folder}")
        print(f"DEBUG [storage_helper]: File={file}, filename={file.filename if file else 'None'}")
        
        if not file or not allowed_file(file.filename):
            print(f"DEBUG [storage_helper]: Invalid file type. File exists: {file is not None}, Allowed: {allowed_file(file.filename) if file else False}")
            raise ValueError("Invalid file type")
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        print(f"DEBUG [storage_helper]: File size: {file_size} bytes")
        
        if file_size > MAX_FILE_SIZE:
            print(f"DEBUG [storage_helper]: File too large: {file_size} > {MAX_FILE_SIZE}")
            raise ValueError("File size exceeds 5MB limit")
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        
        # Build storage path
        storage_path = f"{folder}/{unique_filename}" if folder else unique_filename
        
        print(f"DEBUG [storage_helper]: Storage path: {storage_path}")
        
        # Read file content
        file_content = file.read()
        
        print(f"DEBUG [storage_helper]: File content read, size: {len(file_content)} bytes")
        
        # Upload to Supabase Storage using admin client
        print(f"DEBUG [storage_helper]: Uploading to Supabase...")
        result = supabase_admin.storage.from_(bucket_name).upload(
            path=storage_path,
            file=file_content,
            file_options={
                "content-type": file.content_type or "image/jpeg",
                "upsert": "false"
            }
        )
        
        print(f"DEBUG [storage_helper]: Upload result: {result}")
        
        # Check if upload was successful
        if hasattr(result, 'error') and result.error:
            print(f"DEBUG [storage_helper]: Upload failed with error: {result.error}")
            raise Exception(f"Upload failed: {result.error}")
        
        # Get public URL
        public_url = supabase_admin.storage.from_(bucket_name).get_public_url(storage_path)
        
        print(f"DEBUG [storage_helper]: Public URL generated: {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading to storage: {e}")
        import traceback
        traceback.print_exc()
        return None

def delete_from_storage(url, bucket_name):
    """
    Delete file from Supabase Storage
    
    Args:
        url: Public URL of the file
        bucket_name: Name of the storage bucket
    
    Returns:
        True on success, False on error
    """
    try:
        if not url:
            return True
        
        # Extract path from URL
        # URL format: https://<project>.supabase.co/storage/v1/object/public/<bucket>/<path>
        parts = url.split(f'/storage/v1/object/public/{bucket_name}/')
        if len(parts) < 2:
            return False
        
        file_path = parts[1]
        
        # Delete from storage using admin client
        supabase_admin.storage.from_(bucket_name).remove([file_path])
        
        return True
        
    except Exception as e:
        print(f"Error deleting from storage: {e}")
        return False
