-- Create saved_events table for users to bookmark events
CREATE TABLE IF NOT EXISTS saved_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, user_id)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_saved_events_user_id ON saved_events(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_events_event_id ON saved_events(event_id);

-- Enable RLS
ALTER TABLE saved_events ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (permissive to match other tables)
CREATE POLICY "Allow all operations on saved_events" ON saved_events FOR ALL USING (true);
