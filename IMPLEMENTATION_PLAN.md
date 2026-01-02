# Implementation Plan: Make Everything Real (Data Integration)

## Current Status Analysis

### ✅ **Completed (UI Layer)**
- Landing page with hero and features
- Login/Signup pages (email & phone auth UI)
- Dashboard/Home with AI suggestions section
- Events Discovery page (grid layout, filters)
- Event Detail page (RSVP, comments, attendees UI)
- Groups Discovery page (grid layout, filters)
- Issue Reporting form (photo upload, location, priority)
- My Reports/Issues list page (status filters)
- Profile page (stats, badges, activity, settings tabs)
- Responsive design (mobile to desktop)
- Bottom navigation across all pages
- Material Symbols icons (Outlined + Rounded)

### 🚧 **Missing UI Pages**
- Group Detail page (discussions, member list, join/leave)
- Event Create/Edit form (organizers)
- Group Create/Edit form (organizers)
- Issue Detail page (full timeline, comments)
- Chat/Messages page (conversations list)
- Chat Detail page (1-on-1 or group chat)
- Notifications center page
- Admin dashboard (moderation, analytics)
- Authority/Volunteer dashboard (issue management)
- Search results page (global search)
- Map view page (events, issues on map)
- User public profile page (view others)

### ✅ **Database Schema (Complete)**
- Users table (profile, interests, reputation, verification)
- Events table (with RSVP tracking)
- Groups table (with member roles)
- Issues table (with status tracking)
- Messages table (1-on-1 and group)
- Notifications table
- Proper indexes and RLS policies

### 🚧 **Missing Database Tables**
- `event_comments` - Comments on events
- `group_posts` - Posts/discussions in groups
- `group_post_comments` - Comments on group posts
- `issue_comments` - Comments/updates on issues
- `issue_updates` - Status change history for issues
- `user_badges` - Achievements earned by users
- `user_activity` - Activity log for timeline
- `polls` - Polls in groups
- `poll_votes` - User votes on polls
- `file_uploads` - Shared files in groups
- `event_analytics` - Track event attendance/engagement
- `email_preferences` - User notification preferences

### 🔴 **Backend Not Connected**
- All routes return mock/static data
- No real database queries
- No CRUD operations implemented
- No file upload handling (Supabase Storage)
- No API endpoints for AJAX operations
- No real-time features (Supabase Realtime)

## Gap Analysis by User Story

### **Regular User / Citizen**
| Feature | UI Status | Backend Status | Priority |
|---------|-----------|----------------|----------|
| Create profile | ✅ Signup form | 🔴 Not saving interests/location | HIGH |
| Browse events | ✅ Discovery page | 🔴 Mock data | HIGH |
| RSVP to events | ✅ UI buttons | 🔴 No database | HIGH |
| Join groups | ✅ Discovery page | 🔴 No join logic | HIGH |
| Report issues | ✅ Form complete | 🔴 No submission | HIGH |
| View issue status | ✅ List page | 🔴 Mock data | HIGH |
| Chat with members | 🚧 No UI | 🔴 Not implemented | MEDIUM |
| Notifications | 🚧 Bell icon only | 🔴 Not implemented | MEDIUM |
| Reputation/Points | ✅ Shown in profile | 🔴 Not calculated | LOW |

### **Community Organizer / Event Host**
| Feature | UI Status | Backend Status | Priority |
|---------|-----------|----------------|----------|
| Create events | 🚧 No form | 🔴 Not implemented | HIGH |
| Edit events | 🚧 No form | 🔴 Not implemented | HIGH |
| Create groups | 🚧 No form | 🔴 Not implemented | HIGH |
| Manage group members | 🚧 No UI | 🔴 Not implemented | HIGH |
| Post announcements | 🚧 No UI | 🔴 Not implemented | MEDIUM |
| View analytics | 🚧 No UI | 🔴 Not implemented | LOW |
| Send notifications | 🚧 No UI | 🔴 Not implemented | LOW |

### **Local Authority / Volunteer**
| Feature | UI Status | Backend Status | Priority |
|---------|-----------|----------------|----------|
| View issues on map | 🚧 No map view | 🔴 Not implemented | HIGH |
| Filter issues | ✅ Filter UI | 🔴 Mock data | HIGH |
| Update issue status | 🚧 No UI | 🔴 Not implemented | HIGH |
| Chat with reporter | 🚧 No chat UI | 🔴 Not implemented | MEDIUM |
| AI insights | 🚧 No UI | 🔴 Not implemented | LOW |

### **Admin**
| Feature | UI Status | Backend Status | Priority |
|---------|-----------|----------------|----------|
| Moderate content | 🚧 No admin panel | 🔴 Not implemented | MEDIUM |
| Manage users | 🚧 No admin panel | 🔴 Not implemented | MEDIUM |
| View analytics | 🚧 No admin panel | 🔴 Not implemented | LOW |

### **Cross-Cutting Features**
| Feature | UI Status | Backend Status | Priority |
|---------|-----------|----------------|----------|
| Responsive design | ✅ Complete | N/A | DONE |
| Map integration | 🚧 No map UI | 🔴 Not implemented | HIGH |
| Search | 🚧 Search bars only | 🔴 Not implemented | HIGH |
| AI suggestions | ✅ UI sections | 🔴 Mock data | MEDIUM |
| Push notifications | 🚧 No service worker | 🔴 Not implemented | LOW |
| Email alerts | N/A | 🔴 Not implemented | LOW |

## Implementation Phases (REVISED)

---

## **PHASE 1: User Profile & Authentication** 🔐
**Goal**: Complete user data flow from signup to profile display

### Tasks:
1. **Update User Model** (`app/models.py`)
   - Add `display_name` property
   - Add helper methods: `get_stats()`, `get_badges()`, `get_activity()`
   - Add `bio` field support

2. **Fix Signup Flow** (`app/routes/auth.py`)
   - Save user data to Supabase after Firebase signup
   - Handle location, interests during signup
   - Store user session properly

3. **Profile Page Integration** (`app/routes/profile.py`)
   - Fetch real user data from Supabase
   - Calculate actual stats (events attended, groups joined, etc.)
   - Display real activity timeline
   - Implement profile edit/update

4. **Database Updates**
   - Add `bio` column to users table
   - Add `cover_photo` column to users table
   - Create `user_activity` table for timeline

**Deliverables**: Working profile page with real data, edit functionality

---

## **PHASE 2: Events System** 📅
**Goal**: Full events CRUD with RSVP functionality

### Tasks:
1. **Create Event Model** (`app/models.py`)
   - Event class with CRUD methods
   - RSVP methods
   - Comment methods
   - Attendee list methods

2. **Events Discovery** (`app/routes/events.py`)
   - Fetch events from Supabase with filters (category, date)
   - Search functionality
   - Pagination
   - Sort by date/popularity

3. **Event Detail Page**
   - Fetch event by ID with organizer info
   - Get RSVP list with user details
   - Implement RSVP actions (Going/Maybe)
   - Comments section with real data
   - Similar events recommendations

4. **Create Event Flow**
   - Form for organizers to create events
   - Image upload to Supabase Storage
   - Location picker/geocoding
   - Date/time picker

5. **API Endpoints**
   - POST `/api/events/create` - Create event
   - POST `/api/events/<id>/rsvp` - RSVP to event
   - GET `/api/events/<id>/attendees` - Get attendees
   - POST `/api/events/<id>/comments` - Add comment
   - PUT `/api/events/<id>` - Update event
   - DELETE `/api/events/<id>` - Delete event

**Deliverables**: Complete events system with CRUD, RSVP, comments

---

## **PHASE 3: Groups System** 👥
**Goal**: Full groups functionality with member management

### Tasks:
1. **Create Group Model** (`app/models.py`)
   - Group class with CRUD methods
   - Member management methods
   - Post/discussion methods

2. **Groups Discovery** (`app/routes/groups.py`)
   - Fetch all groups with filters
   - Search functionality
   - Show member counts from database
   - My Groups filter

3. **Group Detail Page**
   - Fetch group by ID
   - Member list with roles
   - Discussion posts
   - Join/Leave functionality
   - Admin controls for group creator

4. **Create Group Flow**
   - Form to create new group
   - Image upload for group icon/cover
   - Category selection
   - Privacy settings

5. **API Endpoints**
   - POST `/api/groups/create` - Create group
   - POST `/api/groups/<id>/join` - Join group
   - POST `/api/groups/<id>/leave` - Leave group
   - GET `/api/groups/<id>/members` - Get members
   - POST `/api/groups/<id>/posts` - Create post
   - PUT `/api/groups/<id>` - Update group
   - DELETE `/api/groups/<id>` - Delete group

**Deliverables**: Complete groups system with discussions

---

## **PHASE 4: Issue Reporting System** 🛠️
**Goal**: Full issue reporting with status tracking

### Tasks:
1. **Create Issue Model** (`app/models.py`)
   - Issue class with CRUD methods
   - Status update methods
   - Comment/update methods

2. **Issue Reporting** (`app/routes/issues.py`)
   - Handle form submission
   - Image upload to Supabase Storage
   - GPS location capture
   - Priority setting

3. **My Reports Page**
   - Fetch user's issues from database
   - Filter by status
   - Real-time status updates
   - Before/after photos for resolved issues

4. **Issue Detail Page**
   - View issue details
   - Status timeline
   - Comments section
   - Admin controls to update status

5. **API Endpoints**
   - POST `/api/issues/submit` - Submit issue
   - GET `/api/issues/user/<user_id>` - Get user's issues
   - PUT `/api/issues/<id>/status` - Update status
   - POST `/api/issues/<id>/comments` - Add comment
   - DELETE `/api/issues/<id>` - Delete issue

**Deliverables**: Complete issue reporting with tracking

---

## **PHASE 5: Dashboard & Recommendations** 🏠
**Goal**: Personalized dashboard with AI recommendations

### Tasks:
1. **Dashboard Data Aggregation**
   - Fetch user's groups
   - Fetch upcoming events (user's RSVPs)
   - Fetch recent activity
   - Fetch user's pending issues

2. **AI Recommendations**
   - Recommend events based on interests
   - Suggest groups based on category preferences
   - Highlight nearby issues

3. **Quick Actions**
   - Show stats (new events, active groups)
   - Recent posts from user's groups
   - Notifications preview

4. **Feed Algorithm**
   - Combine posts from joined groups
   - Show events from friends
   - Community updates

**Deliverables**: Personalized dashboard with real data

---

## **PHASE 6: Notifications & Real-time** 🔔
**Goal**: Keep users engaged with notifications

### Tasks:
1. **Notification System**
   - Create notification on event RSVP
   - Notify on issue status change
   - Notify on group post/comment
   - Notify on event reminder

2. **Notification Display**
   - Fetch unread notifications
   - Mark as read functionality
   - Link to relevant pages

3. **Real-time Updates** (Optional)
   - Supabase Realtime for live notifications
   - Live chat messages
   - Live event updates

**Deliverables**: Working notification system

---

## **PHASE 7: Search & Discovery** 🔍
**Goal**: Powerful search across all content

### Tasks:
1. **Global Search**
   - Search events by keyword, location, category
   - Search groups by name, description
   - Search users by name
   - Search issues by location, category

2. **Filters & Sort**
   - Date range filters
   - Location radius filters
   - Category filters
   - Sort by relevance, date, popularity

3. **Map View**
   - Display events on map
   - Display issues on map
   - Clustering for multiple markers

**Deliverables**: Comprehensive search system

---

## **PHASE 8: Admin & Moderation** 👮
**Goal**: Admin dashboard for content moderation

### Tasks:
1. **Admin Dashboard**
   - View all users, events, groups, issues
   - Moderation queue
   - Analytics overview

2. **Moderation Actions**
   - Approve/reject content
   - Ban users
   - Delete inappropriate content

3. **Analytics**
   - User growth charts
   - Event participation metrics
   - Issue resolution rates

**Deliverables**: Admin panel with moderation tools

---

## Database Schema Extensions Needed

```sql
-- Event Comments
CREATE TABLE event_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Group Posts (Discussions)
CREATE TABLE group_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    author_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT,
    content TEXT NOT NULL,
    post_type TEXT DEFAULT 'discussion' CHECK (post_type IN ('discussion', 'announcement', 'poll')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Group Post Comments
CREATE TABLE group_post_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES group_posts(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Issue Comments/Updates
CREATE TABLE issue_updates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_id UUID REFERENCES issues(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    update_type TEXT DEFAULT 'comment' CHECK (update_type IN ('comment', 'status_change', 'assignment')),
    old_status TEXT,
    new_status TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Badges/Achievements
CREATE TABLE user_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    badge_type TEXT NOT NULL,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Activity Log
CREATE TABLE user_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL,
    entity_type TEXT,
    entity_id UUID,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add missing columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS cover_photo TEXT;
```

## Implementation Order (REVISED - Complete Scope)

### **PHASE 0: Database & Model Foundation** 🗄️
**Goal**: Set up complete database schema and base models
- Run database schema extensions
- Create all model classes (User, Event, Group, Issue, Message, etc.)
- Set up Supabase Storage buckets (avatars, covers, event-images, issue-photos)
- Test database connections

### **PHASE 1: User Profile & Authentication** 🔐
**Goal**: Complete user registration and profile system
- Fix signup to save location, interests, bio to database
- Profile view page - fetch real user data
- Profile edit page - update user info
- Calculate real stats (events attended, groups joined, issues reported)
- Activity timeline from database
- Badge system implementation
- Upload avatar & cover photo to Supabase Storage

### **PHASE 2: Events System (Complete)** 📅
**Goal**: Full event lifecycle from creation to attendance
- **Create Event Form UI** (organizers only)
- **Event CRUD Backend**
  - POST /api/events - Create event
  - GET /api/events - List with filters (date, category, location)
  - GET /api/events/:id - Get single event
  - PUT /api/events/:id - Update event
  - DELETE /api/events/:id - Delete event
- **RSVP System**
  - POST /api/events/:id/rsvp - RSVP (going/interested)
  - GET /api/events/:id/attendees - Get attendee list
- **Comments**
  - POST /api/events/:id/comments - Add comment
  - GET /api/events/:id/comments - Get comments
- **Image Upload** - Event cover photos to Supabase Storage
- **Search & Filters** - Working filters and search
- **Recommendations** - Suggest events based on interests

### **PHASE 3: Groups System (Complete)** 👥
**Goal**: Full group functionality with discussions
- **Create Group Form UI**
- **Group Detail Page UI** - Discussions, members, about
- **Group CRUD Backend**
  - POST /api/groups - Create group
  - GET /api/groups - List with filters
  - GET /api/groups/:id - Get single group
  - PUT /api/groups/:id - Update group
  - DELETE /api/groups/:id - Delete group
- **Member Management**
  - POST /api/groups/:id/join - Join group
  - DELETE /api/groups/:id/leave - Leave group
  - GET /api/groups/:id/members - Get members
  - PUT /api/groups/:id/members/:user_id - Update role (admin only)
- **Discussions**
  - POST /api/groups/:id/posts - Create post
  - GET /api/groups/:id/posts - Get posts
  - POST /api/groups/:id/posts/:post_id/comments - Comment on post
- **Polls** (bonus feature)
- **File Sharing** (bonus feature)

### **PHASE 4: Issue Reporting (Complete)** 🛠️
**Goal**: Full issue lifecycle with tracking
- **Issue Detail Page UI** - Full timeline, comments, status updates
- **Issue Submission Backend**
  - POST /api/issues - Submit issue with photo upload
  - GET /api/issues/user/:user_id - Get user's issues
  - GET /api/issues - List all issues (with filters)
  - GET /api/issues/:id - Get single issue
  - PUT /api/issues/:id/status - Update status (authority/admin only)
- **Comments/Updates**
  - POST /api/issues/:id/updates - Add update/comment
  - GET /api/issues/:id/updates - Get update timeline
- **GPS Location** - Capture and save coordinates
- **Photo Upload** - To Supabase Storage
- **Before/After Photos** - For resolved issues
- **Map View UI** - Show issues on map

### **PHASE 5: Chat & Messaging** 💬
**Goal**: Real-time communication
- **Conversations List UI** - Show all chats
- **Chat Detail UI** - Message thread
- **Backend**
  - POST /api/messages - Send message
  - GET /api/messages/conversations - Get user's conversations
  - GET /api/messages/:conversation_id - Get messages
- **Real-time** - Supabase Realtime for live messages
- **Group Chat** - Messages in group context
- **Notifications** - New message alerts

### **PHASE 6: Dashboard & Personalization** 🏠
**Goal**: Personalized feed and recommendations
- **Dashboard Backend**
  - Fetch user's upcoming events (RSVPs)
  - Fetch user's groups with recent posts
  - Fetch user's pending issues
  - Fetch recommendations (events, groups)
- **AI Recommendations Algorithm**
  - Match events to user interests
  - Suggest nearby events
  - Suggest groups based on interests
- **Activity Feed** - Posts from joined groups
- **Quick Stats** - Real-time counts

### **PHASE 7: Notifications System** 🔔
**Goal**: Keep users engaged and informed
- **Notifications Center UI**
- **Backend**
  - Create notifications on: RSVP, group join, issue status change, comments
  - GET /api/notifications - Get user's notifications
  - PUT /api/notifications/:id/read - Mark as read
  - PUT /api/notifications/read-all - Mark all read
- **Real-time** - Supabase Realtime for live notifications
- **Email Notifications** (optional) - Send emails for important updates
- **Notification Preferences** - User settings for what to receive

### **PHASE 8: Search & Discovery** 🔍
**Goal**: Help users find what they need
- **Search Results Page UI**
- **Global Search Backend**
  - GET /api/search?q=query&type=events|groups|users|issues
  - Full-text search across all entities
- **Advanced Filters**
  - Location radius search
  - Date range filters
  - Category filters
- **Map View Integration**
  - Show events on map with clustering
  - Show issues on map with category markers
  - Click marker to see details

### **PHASE 9: Organizer Tools** 🎯
**Goal**: Empower community organizers
- **Event Management Dashboard UI** - List organizer's events
- **Group Management Dashboard UI** - Manage members, approve posts
- **Analytics UI** - Event attendance, group engagement
- **Backend**
  - GET /api/organizer/events - Get organizer's events with stats
  - GET /api/organizer/groups - Get managed groups
  - GET /api/analytics/event/:id - Event analytics
  - GET /api/analytics/group/:id - Group analytics
- **Announcements** - Send notifications to group members
- **Member Approval** - For private groups

### **PHASE 10: Authority/Volunteer Dashboard** 👮
**Goal**: Issue management for authorities
- **Authority Dashboard UI** - Issue queue, map view, filters
- **Backend**
  - GET /api/authority/issues - Get issues with filters
  - PUT /api/authority/issues/:id/assign - Assign to volunteer
  - PUT /api/authority/issues/:id/status - Update status
  - GET /api/authority/analytics - Issue resolution metrics
- **Map View** - Interactive issue map
- **AI Insights** (bonus) - Detect recurring issues, hotspots

### **PHASE 11: Admin Panel** 🛡️
**Goal**: Platform moderation and management
- **Admin Dashboard UI** - Overview, moderation queue
- **User Management UI** - List, ban, verify users
- **Content Moderation UI** - Review flagged content
- **Analytics UI** - Platform metrics
- **Backend**
  - GET /api/admin/users - User management
  - PUT /api/admin/users/:id/ban - Ban user
  - PUT /api/admin/users/:id/verify - Verify user
  - DELETE /api/admin/content/:type/:id - Delete content
  - GET /api/admin/analytics - Platform analytics

### **PHASE 12: Gamification & Engagement** 🏆
**Goal**: Encourage participation
- **Leaderboard UI** - Top contributors
- **Badge System** - Visual badges on profile
- **Backend**
  - Reputation points calculation logic
  - Badge awarding on milestones
  - GET /api/leaderboard - Top users
- **Achievements** - Track and display user achievements

### **PHASE 13: Polish & Optimization** ✨
**Goal**: Production-ready
- **Performance Optimization** - Query optimization, caching
- **Error Handling** - User-friendly error messages
- **Loading States** - Skeleton screens, spinners
- **Offline Support** (PWA) - Service worker, caching
- **Image Optimization** - Compress uploads, lazy loading
- **Security Audit** - RLS policies, input validation
- **Testing** - Unit tests, integration tests
- **Documentation** - API docs, user guide

---

## Sprint Planning (Recommended Timeline)

### **SPRINT 1 (2-3 weeks)** - Foundation ⭐ START HERE
- ✅ Phase 0: Database & Models
- ✅ Phase 1: User Profile & Auth
- Focus: Get core user system working with real data

### **SPRINT 2 (2-3 weeks)** - Core Features
- ✅ Phase 2: Events System (Complete)
- ✅ Phase 3: Groups System (Complete)
- Focus: Main engagement features working

### **SPRINT 3 (2 weeks)** - Community Features  
- ✅ Phase 4: Issue Reporting (Complete)
- ✅ Phase 5: Chat & Messaging
- Focus: Community interaction

### **SPRINT 4 (1-2 weeks)** - Intelligence
- ✅ Phase 6: Dashboard & Personalization
- ✅ Phase 7: Notifications
- Focus: Keep users engaged

### **SPRINT 5 (2 weeks)** - Discovery
- ✅ Phase 8: Search & Discovery
- ✅ Phase 9: Organizer Tools
- Focus: Help users find content

### **SPRINT 6 (1-2 weeks)** - Management
- ✅ Phase 10: Authority Dashboard
- ✅ Phase 11: Admin Panel
- Focus: Platform management

### **SPRINT 7 (1 week)** - Engagement
- ✅ Phase 12: Gamification
- Focus: Encourage participation

### **SPRINT 8 (1-2 weeks)** - Production Ready
- ✅ Phase 13: Polish & Optimization
- Focus: Launch-ready platform

**Total Estimated Time: 12-16 weeks for full platform**

---

## Technical Stack Summary
- **Backend**: Flask 3.0.0 + Python 3.12
- **Database**: PostgreSQL (Supabase)
- **Authentication**: Firebase Auth (email + phone)
- **Storage**: Supabase Storage (images, files)
- **Real-time**: Supabase Realtime (chat, notifications)
- **Frontend**: Jinja2 templates + Tailwind CSS
- **Icons**: Material Symbols (Outlined + Rounded)
- **Maps**: Google Maps API or Mapbox (to be integrated)
- **Deployment**: Gunicorn + Nginx (or Vercel/Railway)

---

## Missing Templates Needed

### Critical (Need to Build)
1. `events/create.html` - Create event form
2. `events/edit.html` - Edit event form
3. `groups/detail.html` - Group page with discussions
4. `groups/create.html` - Create group form
5. `issues/detail.html` - Issue detail with timeline
6. `chat/conversations.html` - Chat list
7. `chat/detail.html` - Chat thread
8. `notifications/list.html` - Notifications center
9. `search/results.html` - Search results page
10. `map/view.html` - Map view for events/issues

### Important (Organizers)
11. `organizer/events.html` - Event management dashboard
12. `organizer/groups.html` - Group management dashboard
13. `organizer/analytics.html` - Analytics view

### Important (Authority)
14. `authority/dashboard.html` - Issue management dashboard
15. `authority/map.html` - Issue map view

### Important (Admin)
16. `admin/dashboard.html` - Admin overview
17. `admin/users.html` - User management
18. `admin/moderation.html` - Content moderation
19. `admin/analytics.html` - Platform analytics

### Nice to Have
20. `profile/public.html` - View other user's profile
21. `leaderboard.html` - Top contributors
22. `help.html` - User guide/FAQ

---

## Next Steps - PHASE 0 & 1

**Immediate Actions:**
1. ✅ Run database schema extensions (add missing tables)
2. ✅ Set up Supabase Storage buckets
3. ✅ Update User model with new fields (bio, cover_photo)
4. ✅ Create Event, Group, Issue models
5. ✅ Fix signup to save complete user data
6. ✅ Connect profile page to real database
7. ✅ Implement profile edit with file uploads

**Ready to start Phase 0 & 1?** This establishes the foundation for everything else.
