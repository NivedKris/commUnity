-- CommUnity App - Database Schema Extensions
-- Run this AFTER running the main database_schema.sql

-- Add missing columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS cover_photo TEXT;

-- Event Comments
CREATE TABLE IF NOT EXISTS event_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_event_comments_event ON event_comments(event_id);
CREATE INDEX IF NOT EXISTS idx_event_comments_user ON event_comments(user_id);

-- Group Posts (Discussions)
CREATE TABLE IF NOT EXISTS group_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    author_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT,
    content TEXT NOT NULL,
    post_type TEXT DEFAULT 'discussion' CHECK (post_type IN ('discussion', 'announcement', 'poll')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_group_posts_group ON group_posts(group_id);
CREATE INDEX IF NOT EXISTS idx_group_posts_author ON group_posts(author_id);

-- Group Post Comments
CREATE TABLE IF NOT EXISTS group_post_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES group_posts(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_group_post_comments_post ON group_post_comments(post_id);
CREATE INDEX IF NOT EXISTS idx_group_post_comments_user ON group_post_comments(user_id);

-- Issue Updates (Comments and Status Changes)
CREATE TABLE IF NOT EXISTS issue_updates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_id UUID REFERENCES issues(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    update_type TEXT DEFAULT 'comment' CHECK (update_type IN ('comment', 'status_change', 'assignment')),
    old_status TEXT,
    new_status TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_issue_updates_issue ON issue_updates(issue_id);
CREATE INDEX IF NOT EXISTS idx_issue_updates_user ON issue_updates(user_id);

-- User Badges/Achievements
CREATE TABLE IF NOT EXISTS user_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    badge_type TEXT NOT NULL CHECK (badge_type IN (
        'first_steps', 'event_explorer', 'community_builder', 
        'problem_solver', 'conversation_starter', 'super_star',
        'event_host', 'group_creator', 'helpful_neighbor'
    )),
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, badge_type)
);

CREATE INDEX IF NOT EXISTS idx_user_badges_user ON user_badges(user_id);

-- User Activity Log
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    activity_type TEXT NOT NULL CHECK (activity_type IN (
        'joined', 'event_rsvp', 'event_attended', 'group_joined', 
        'issue_reported', 'comment_posted', 'badge_earned'
    )),
    entity_type TEXT CHECK (entity_type IN ('event', 'group', 'issue', 'post', 'badge')),
    entity_id UUID,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_activity_user ON user_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_type ON user_activity(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activity_created ON user_activity(created_at DESC);

-- Polls (for groups)
CREATE TABLE IF NOT EXISTS polls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    creator_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    options TEXT[] NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_polls_group ON polls(group_id);

-- Poll Votes
CREATE TABLE IF NOT EXISTS poll_votes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    poll_id UUID REFERENCES polls(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    option_index INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(poll_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_poll_votes_poll ON poll_votes(poll_id);

-- File Uploads (for group resource sharing)
CREATE TABLE IF NOT EXISTS file_uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    uploader_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_size BIGINT,
    file_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_file_uploads_group ON file_uploads(group_id);

-- Email Preferences
CREATE TABLE IF NOT EXISTS email_preferences (
    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    event_reminders BOOLEAN DEFAULT TRUE,
    group_updates BOOLEAN DEFAULT TRUE,
    issue_updates BOOLEAN DEFAULT TRUE,
    weekly_digest BOOLEAN DEFAULT FALSE,
    marketing_emails BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on new tables
ALTER TABLE event_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_post_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE issue_updates ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE polls ENABLE ROW LEVEL SECURITY;
ALTER TABLE poll_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_preferences ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (allow all for now - tighten in production)
CREATE POLICY "Allow all on event_comments" ON event_comments FOR ALL USING (true);
CREATE POLICY "Allow all on group_posts" ON group_posts FOR ALL USING (true);
CREATE POLICY "Allow all on group_post_comments" ON group_post_comments FOR ALL USING (true);
CREATE POLICY "Allow all on issue_updates" ON issue_updates FOR ALL USING (true);
CREATE POLICY "Allow all on user_badges" ON user_badges FOR ALL USING (true);
CREATE POLICY "Allow all on user_activity" ON user_activity FOR ALL USING (true);
CREATE POLICY "Allow all on polls" ON polls FOR ALL USING (true);
CREATE POLICY "Allow all on poll_votes" ON poll_votes FOR ALL USING (true);
CREATE POLICY "Allow all on file_uploads" ON file_uploads FOR ALL USING (true);
CREATE POLICY "Allow all on email_preferences" ON email_preferences FOR ALL USING (true);

-- Apply updated_at triggers
CREATE TRIGGER update_group_posts_updated_at BEFORE UPDATE ON group_posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default badges data for reference
COMMENT ON TABLE user_badges IS 'Badge types: first_steps (joined), event_explorer (10 events), community_builder (5 groups), problem_solver (10 issues), conversation_starter (50 comments), super_star (1000 points), event_host (created event), group_creator (created group), helpful_neighbor (helped in discussions)';
