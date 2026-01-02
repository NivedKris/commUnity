# Phase 0 & 1 Setup Guide

## ✅ COMPLETED

### 1. Database Schema Extensions
- Created `/database_schema_extensions.sql` with all missing tables
- Added columns: `bio`, `cover_photo` to users table
- New tables: event_comments, group_posts, issue_updates, user_badges, user_activity, polls, file_uploads, email_preferences

### 2. Models Complete
- Updated `User` model with:
  - New fields: bio, cover_photo, display_name
  - `get_stats()` - calculates real stats from database
  - `get_badges()` - fetches earned badges
  - `get_activity()` - fetches recent activity timeline
  - Enhanced `create()` - logs activity & awards first badge
  - Enhanced `update()` - updates instance attributes

- Created `Event` model with:
  - `create()` - create event with activity logging
  - `get_by_id()` - fetch single event
  - `get_all()` - fetch all events with filters
  - `get_attendees()` - get RSVP list
  - `get_attendee_count()` - count attendees

- Created `Group` model with:
  - `create()` - create group, add creator as admin, log activity
  - `get_by_id()` - fetch single group
  - `get_all()` - fetch all groups with filters
  - `get_member_count()` - count members

- Created `Issue` model with:
  - `create()` - create issue with activity logging
  - `get_by_id()` - fetch single issue
  - `get_all()` - fetch all issues with filters
  - `update_status()` - change status with logging

## 🚀 NEXT STEPS

### Step 1: Run Database Extensions
```bash
# Go to your Supabase project dashboard
# SQL Editor → New query
# Copy contents of database_schema_extensions.sql
# Run the query
```

### Step 2: Set up Supabase Storage Buckets
Go to Supabase Dashboard → Storage → Create buckets:
- `avatars` - For user profile pictures
- `covers` - For user cover photos  
- `event-images` - For event cover images
- `group-images` - For group icons/covers
- `issue-photos` - For issue report photos

Set bucket policies to public read:
```sql
-- For each bucket, run:
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'avatars');

CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'avatars');
```

### Step 3: Update Routes to Use Models
Now we can update routes to use real data:

**Profile Page** - Fetch real user data and stats
**Events Discovery** - Query events from database
**Groups Discovery** - Query groups from database  
**Issues List** - Query user's issues

### Step 4: Test Database Connection
```bash
cd /home/turing/community
python
>>> from app.utils.supabase_client import supabase
>>> response = supabase.table('users').select('*').limit(1).execute()
>>> print(response.data)
```

## 📋 Ready to Continue

After running the database extensions and setting up storage buckets, we can:
1. Fix signup to save complete user data (location, interests, bio)
2. Connect profile page to fetch real stats and activity
3. Update events/groups pages to show real data

**Let me know when database extensions are run and we'll continue!**
