"""Complete seeding script: users, events, and RSVPs"""
from app.utils.supabase_client import supabase
from datetime import datetime, timedelta
import random
import uuid

# Sample users data
users_data = [
    {
        'name': 'Priya Sharma',
        'email': 'priya.sharma@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Technology', 'Education', 'Health & Wellness'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=1'
    },
    {
        'name': 'Rahul Kumar',
        'email': 'rahul.kumar@example.com',
        'location': 'Kochi, Kerala',
        'interests': ['Sports & Fitness', 'Music', 'Food & Dining'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=12'
    },
    {
        'name': 'Ananya Menon',
        'email': 'ananya.menon@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Arts & Culture', 'Environment', 'Education'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=5'
    },
    {
        'name': 'Vikram Nair',
        'email': 'vikram.nair@example.com',
        'location': 'Kollam, Kerala',
        'interests': ['Technology', 'Sports & Fitness', 'Music'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=13'
    },
    {
        'name': 'Divya Krishnan',
        'email': 'divya.krishnan@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Health & Wellness', 'Food & Dining', 'Arts & Culture'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=9'
    },
    {
        'name': 'Arjun Pillai',
        'email': 'arjun.pillai@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Environment', 'Technology', 'Sports & Fitness'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=14'
    },
    {
        'name': 'Sneha Reddy',
        'email': 'sneha.reddy@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Education', 'Arts & Culture', 'Health & Wellness'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=10'
    },
    {
        'name': 'Karthik Iyer',
        'email': 'karthik.iyer@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Technology', 'Music', 'Food & Dining'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=15'
    },
    {
        'name': 'Meera Das',
        'email': 'meera.das@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Arts & Culture', 'Education', 'Environment'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=16'
    },
    {
        'name': 'Aditya Varma',
        'email': 'aditya.varma@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Sports & Fitness', 'Technology', 'Music'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=17'
    },
    {
        'name': 'Lakshmi Nair',
        'email': 'lakshmi.nair@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Health & Wellness', 'Food & Dining', 'Education'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=20'
    },
    {
        'name': 'Rohan Bhat',
        'email': 'rohan.bhat@example.com',
        'location': 'Trivandrum, Kerala',
        'interests': ['Technology', 'Environment', 'Sports & Fitness'],
        'user_type': 'citizen',
        'profile_picture': 'https://i.pravatar.cc/150?img=18'
    }
]

# Sample events data
events_data = [
    {
        'title': 'Downtown Tech Meetup 2025',
        'description': 'Connect with local developers and designers. Join us for an evening of networking, learning, and collaboration. Free pizza and drinks included! Topics: AI, Web3, Cloud Computing, and Mobile Development.',
        'category': 'Technology',
        'location': 'Tech Hub, Downtown Trivandrum',
        'latitude': 8.5241,
        'longitude': 76.9366,
        'image_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
        'max_participants': 50,
        'date_time': (datetime.now() + timedelta(days=2, hours=18)).isoformat()
    },
    {
        'title': 'Community Beach Cleanup',
        'description': 'Help keep our beaches clean! Bring gloves and bags, we provide all other equipment. Great for families and all ages. Make a difference in our community while enjoying the beach.',
        'category': 'Environment',
        'location': 'Kovalam Beach',
        'latitude': 8.4004,
        'longitude': 76.9784,
        'image_url': 'https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800',
        'max_participants': 100,
        'date_time': (datetime.now() + timedelta(days=5, hours=7)).isoformat()
    },
    {
        'title': 'Yoga in the Park',
        'description': 'Start your weekend right with outdoor yoga. All levels welcome. Bring your own mat. Professional instructor will guide through various poses and breathing techniques.',
        'category': 'Health & Wellness',
        'location': 'Central Park, Trivandrum',
        'latitude': 8.5123,
        'longitude': 76.9544,
        'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800',
        'max_participants': 30,
        'date_time': (datetime.now() + timedelta(days=3, hours=6)).isoformat()
    },
    {
        'title': 'Local Food Festival',
        'description': 'Taste the best of local cuisine! Over 20 food vendors, live music, and family activities. Experience Kerala\'s rich culinary heritage with traditional and modern dishes.',
        'category': 'Food & Dining',
        'location': 'City Square, Trivandrum',
        'latitude': 8.5074,
        'longitude': 76.9574,
        'image_url': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800',
        'max_participants': 500,
        'date_time': (datetime.now() + timedelta(days=7, hours=11)).isoformat()
    },
    {
        'title': 'Photography Walk',
        'description': 'Explore the city through your lens. Beginners and professionals welcome. Meet at the old town. Capture the historic architecture and vibrant street life.',
        'category': 'Arts & Culture',
        'location': 'Old Town Heritage Area',
        'latitude': 8.4875,
        'longitude': 76.9486,
        'image_url': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800',
        'max_participants': 25,
        'date_time': (datetime.now() + timedelta(days=4, hours=16)).isoformat()
    },
    {
        'title': 'Book Club: Modern Fiction',
        'description': 'Monthly book club discussion. This month: "The Midnight Library" by Matt Haig. Coffee and snacks provided. Deep dive into themes and character analysis.',
        'category': 'Education',
        'location': 'City Library, Trivandrum',
        'latitude': 8.5124,
        'longitude': 76.9513,
        'image_url': 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800',
        'max_participants': 20,
        'date_time': (datetime.now() + timedelta(days=10, hours=17)).isoformat()
    },
    {
        'title': 'Community Sports Day',
        'description': 'Fun sports activities for all ages. Football, cricket, volleyball and more. Bring your family! Prizes for winners and participation certificates for all.',
        'category': 'Sports & Fitness',
        'location': 'Municipal Stadium, Trivandrum',
        'latitude': 8.5289,
        'longitude': 76.9338,
        'image_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800',
        'max_participants': 200,
        'date_time': (datetime.now() + timedelta(days=6, hours=9)).isoformat()
    },
    {
        'title': 'Music Jam Session',
        'description': 'Open mic and jam session for local musicians. Bring your instruments or just come listen! All genres welcome. Connect with fellow music lovers.',
        'category': 'Music',
        'location': 'Harmony Cafe, Trivandrum',
        'latitude': 8.5041,
        'longitude': 76.9479,
        'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800',
        'max_participants': 40,
        'date_time': (datetime.now() + timedelta(days=8, hours=19)).isoformat()
    },
    {
        'title': 'Coding Workshop for Beginners',
        'description': 'Learn the basics of Python programming. No prior experience needed. Laptops will be provided. Free workshop for aspiring developers.',
        'category': 'Technology',
        'location': 'Innovation Center, Technopark',
        'latitude': 8.5485,
        'longitude': 76.8994,
        'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
        'max_participants': 35,
        'date_time': (datetime.now() + timedelta(days=9, hours=14)).isoformat()
    },
    {
        'title': 'Plant a Tree Drive',
        'description': 'Join us in making Trivandrum greener! We\'ll plant 100+ trees. Tools and saplings provided. Refreshments included. Every tree makes a difference.',
        'category': 'Environment',
        'location': 'Napier Museum Grounds',
        'latitude': 8.4962,
        'longitude': 76.9529,
        'image_url': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800',
        'max_participants': 80,
        'date_time': (datetime.now() + timedelta(days=11, hours=8)).isoformat()
    },
    {
        'title': 'Marathon for Health',
        'description': '5K and 10K runs for all fitness levels. T-shirts and medals for all participants. Support local health initiatives. Professional timing and medical support.',
        'category': 'Sports & Fitness',
        'location': 'Trivandrum City Center',
        'latitude': 8.5062,
        'longitude': 76.9570,
        'image_url': 'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800',
        'max_participants': 300,
        'date_time': (datetime.now() + timedelta(days=14, hours=6)).isoformat()
    },
    {
        'title': 'Art Exhibition: Local Artists',
        'description': 'Showcase of paintings, sculptures, and digital art by talented local artists. Free entry. Meet the artists and purchase original works.',
        'category': 'Arts & Culture',
        'location': 'Kanakakunnu Palace',
        'latitude': 8.5133,
        'longitude': 76.9478,
        'image_url': 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800',
        'max_participants': 150,
        'date_time': (datetime.now() + timedelta(days=12, hours=10)).isoformat()
    }
]

def clear_events():
    """Delete all existing events and RSVPs"""
    try:
        print("🗑️  Clearing existing RSVPs...")
        supabase.table('event_rsvps').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("🗑️  Clearing existing events...")
        supabase.table('events').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("✅ Cleared all existing events and RSVPs\n")
    except Exception as e:
        print(f"❌ Error clearing data: {e}\n")

def seed_users():
    """Create sample users"""
    print("👥 Seeding users...")
    created_users = []
    
    for user_data in users_data:
        try:
            # Check if user already exists
            existing = supabase.table('users').select('*').eq('email', user_data['email']).execute()
            if existing.data and len(existing.data) > 0:
                print(f"  ⏭️  User already exists: {user_data['name']}")
                created_users.append(existing.data[0])
                continue
            
            # Create new user
            user_record = {
                'id': str(uuid.uuid4()),
                'email': user_data['email'],
                'name': user_data['name'],
                'location': user_data['location'],
                'interests': user_data['interests'],
                'user_type': user_data['user_type'],
                'profile_picture': user_data['profile_picture'],
                'reputation_points': random.randint(50, 500)
            }
            
            response = supabase.table('users').insert(user_record).execute()
            if response.data:
                print(f"  ✅ Created: {user_data['name']}")
                created_users.append(response.data[0])
        except Exception as e:
            print(f"  ❌ Error creating {user_data['name']}: {e}")
    
    print(f"\n✅ Total users available: {len(created_users)}\n")
    return created_users

def seed_events(users):
    """Create sample events with random organizers"""
    print("📅 Seeding events...")
    created_events = []
    
    for event_data in events_data:
        try:
            # Randomly select an organizer
            organizer = random.choice(users)
            
            event_record = {
                'id': str(uuid.uuid4()),
                'organizer_id': organizer['id'],
                'title': event_data['title'],
                'description': event_data['description'],
                'category': event_data['category'],
                'date_time': event_data['date_time'],
                'location': event_data['location'],
                'latitude': event_data['latitude'],
                'longitude': event_data['longitude'],
                'max_participants': event_data['max_participants'],
                'image_url': event_data['image_url']
            }
            
            response = supabase.table('events').insert(event_record).execute()
            if response.data:
                event = response.data[0]
                print(f"  ✅ Created: {event_data['title']} (by {organizer['name']})")
                created_events.append(event)
        except Exception as e:
            print(f"  ❌ Error creating {event_data['title']}: {e}")
    
    print(f"\n✅ Created {len(created_events)} events\n")
    return created_events

def seed_rsvps(users, events):
    """Create RSVPs for events"""
    print("🎫 Seeding RSVPs...")
    created_rsvps = 0
    
    for event in events:
        # Randomly select 30-70% of users to RSVP
        rsvp_count = random.randint(int(len(users) * 0.3), int(len(users) * 0.7))
        rsvp_users = random.sample(users, rsvp_count)
        
        for user in rsvp_users:
            # Don't let organizer RSVP to their own event
            if user['id'] == event['organizer_id']:
                continue
            
            try:
                # 70% going, 30% interested
                status = 'going' if random.random() < 0.7 else 'interested'
                
                rsvp_record = {
                    'id': str(uuid.uuid4()),
                    'event_id': event['id'],
                    'user_id': user['id'],
                    'status': status
                }
                
                response = supabase.table('event_rsvps').insert(rsvp_record).execute()
                if response.data:
                    created_rsvps += 1
            except Exception as e:
                print(f"  ❌ Error creating RSVP: {e}")
        
        print(f"  ✅ {event['title'][:40]}... - {rsvp_count} RSVPs")
    
    print(f"\n✅ Created {created_rsvps} total RSVPs\n")

def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 COMPLETE DATABASE SEEDING")
    print("="*60 + "\n")
    
    # Clear existing events
    clear_events()
    
    # Seed users
    users = seed_users()
    if not users:
        print("❌ No users created. Exiting.")
        return
    
    # Seed events
    events = seed_events(users)
    if not events:
        print("❌ No events created. Exiting.")
        return
    
    # Seed RSVPs
    seed_rsvps(users, events)
    
    print("="*60)
    print("🎉 SEEDING COMPLETE!")
    print(f"   - {len(users)} users")
    print(f"   - {len(events)} events")
    print(f"   - Multiple RSVPs created")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
