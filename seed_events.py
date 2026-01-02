"""Seed sample events for testing"""
from app.models import Event
from datetime import datetime, timedelta

# Sample events data
events_data = [
    {
        'title': 'Downtown Tech Meetup 2025',
        'description': 'Connect with local developers and designers. Join us for an evening of networking, learning, and collaboration. Free pizza and drinks included!',
        'category': 'Technology',
        'location': 'Tech Hub, Downtown',
        'latitude': 8.5241,
        'longitude': 76.9366,
        'image_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
        'max_participants': 50,
        'date_time': (datetime.now() + timedelta(days=2)).isoformat()
    },
    {
        'title': 'Community Beach Cleanup',
        'description': 'Help keep our beaches clean! Bring gloves and bags, we provide all other equipment. Great for families and all ages.',
        'category': 'Environment',
        'location': 'Kovalam Beach',
        'latitude': 8.4004,
        'longitude': 76.9784,
        'image_url': 'https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800',
        'max_participants': 100,
        'date_time': (datetime.now() + timedelta(days=5)).isoformat()
    },
    {
        'title': 'Yoga in the Park',
        'description': 'Start your weekend right with outdoor yoga. All levels welcome. Bring your own mat.',
        'category': 'Health & Wellness',
        'location': 'Central Park',
        'latitude': 8.5123,
        'longitude': 76.9544,
        'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800',
        'max_participants': 30,
        'date_time': (datetime.now() + timedelta(days=3)).isoformat()
    },
    {
        'title': 'Local Food Festival',
        'description': 'Taste the best of local cuisine! Over 20 food vendors, live music, and family activities.',
        'category': 'Food & Dining',
        'location': 'City Square',
        'latitude': 8.5074,
        'longitude': 76.9574,
        'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800',
        'max_participants': 500,
        'date_time': (datetime.now() + timedelta(days=7)).isoformat()
    },
    {
        'title': 'Photography Walk',
        'description': 'Explore the city through your lens. Beginners and professionals welcome. Meet at the old town.',
        'category': 'Arts & Culture',
        'location': 'Old Town Heritage Area',
        'latitude': 8.4875,
        'longitude': 76.9486,
        'image_url': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800',
        'max_participants': 25,
        'date_time': (datetime.now() + timedelta(days=4)).isoformat()
    },
    {
        'title': 'Book Club: Modern Fiction',
        'description': 'Monthly book club discussion. This month: "The Midnight Library". Coffee and snacks provided.',
        'category': 'Education',
        'location': 'City Library',
        'latitude': 8.5124,
        'longitude': 76.9513,
        'image_url': 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800',
        'max_participants': 20,
        'date_time': (datetime.now() + timedelta(days=10)).isoformat()
    },
    {
        'title': 'Community Sports Day',
        'description': 'Fun sports activities for all ages. Football, cricket, volleyball and more. Bring your family!',
        'category': 'Sports & Fitness',
        'location': 'Municipal Stadium',
        'latitude': 8.5289,
        'longitude': 76.9338,
        'image_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800',
        'max_participants': 200,
        'date_time': (datetime.now() + timedelta(days=6)).isoformat()
    },
    {
        'title': 'Music Jam Session',
        'description': 'Open mic and jam session for local musicians. Bring your instruments or just come listen!',
        'category': 'Music',
        'location': 'Harmony Cafe',
        'latitude': 8.5041,
        'longitude': 76.9479,
        'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800',
        'max_participants': 40,
        'date_time': (datetime.now() + timedelta(days=8)).isoformat()
    }
]

def seed_events(organizer_id):
    """Create sample events"""
    print(f"Creating sample events with organizer_id: {organizer_id}")
    
    created_events = []
    for event_data in events_data:
        try:
            event = Event.create(
                organizer_id=organizer_id,
                title=event_data['title'],
                description=event_data['description'],
                category=event_data['category'],
                date_time=event_data['date_time'],
                location=event_data['location'],
                latitude=event_data['latitude'],
                longitude=event_data['longitude'],
                max_participants=event_data['max_participants'],
                image_url=event_data['image_url']
            )
            if event:
                print(f"✅ Created: {event.title}")
                created_events.append(event)
            else:
                print(f"❌ Failed to create: {event_data['title']}")
        except Exception as e:
            print(f"❌ Error creating {event_data['title']}: {e}")
    
    print(f"\n✅ Successfully created {len(created_events)} events")
    return created_events

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: uv run seed_events.py <your_user_id>")
        print("Get your user ID from the profile page or database")
        sys.exit(1)
    
    organizer_id = sys.argv[1]
    seed_events(organizer_id)
