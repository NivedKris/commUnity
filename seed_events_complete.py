#!/usr/bin/env python3
"""
Comprehensive Event Seeding Script
Seeds 20+ diverse, realistic events with proper RSVPs and attendees
"""

import os
import sys
from datetime import datetime, timedelta
from supabase import create_client
import random

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Event images - diverse, high quality
EVENT_IMAGES = [
    "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1600",  # Tech meetup
    "https://images.unsplash.com/photo-1429962714451-bb934ecdc4ec?w=1600",  # Concert
    "https://images.unsplash.com/photo-1528605248644-14dd04022da1?w=1600",  # Yoga/fitness
    "https://images.unsplash.com/photo-1511578314322-379afb476865?w=1600",  # Art gallery
    "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=1600",  # Networking
    "https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=1600",  # Outdoor activity
    "https://images.unsplash.com/photo-1505236858219-8359eb29e329?w=1600",  # Food event
    "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=1600",  # Workshop
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600",  # Community
    "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=1600",  # Music
    "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=1600",  # Sports
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1600",  # Business
    "https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=1600",  # Beach/outdoor
    "https://images.unsplash.com/photo-1551818255-e6e10975bc17?w=1600",  # Running/marathon
    "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1600",  # Nature/hiking
]

# Comprehensive event data
EVENTS_DATA = [
    {
        "title": "Tech Innovators Summit 2026",
        "description": "Join us for an evening of networking and insights into the future of technology. The Tech Innovators Summit brings together industry leaders, startups, and investors to discuss emerging trends in AI, blockchain, and sustainable tech. Network with 200+ attendees, enjoy keynote speeches from top innovators, and participate in interactive workshops. Free snacks and drinks included!",
        "category": "Technology",
        "location": "Moscone Center, 747 Howard St, San Francisco, CA",
        "date_offset": 2,  # 2 days from now
        "max_participants": 250,
        "latitude": 37.7839,
        "longitude": -122.4015,
        "going_count": 124,
        "interested_count": 56
    },
    {
        "title": "Indie Rock Night Live",
        "description": "Experience an unforgettable night of live indie rock music featuring three amazing local bands. The Velvet Lounge presents an evening of raw energy, authentic sound, and incredible vibes. Doors open at 7:30 PM, first band starts at 8:00 PM sharp. Full bar available, 21+ only. Get your tickets early as this event always sells out!",
        "category": "Music",
        "location": "The Velvet Lounge, 443 Broadway, SF",
        "date_offset": 5,
        "max_participants": 180,
        "latitude": 37.7983,
        "longitude": -122.4068,
        "going_count": 128,
        "interested_count": 89
    },
    {
        "title": "Sunday Morning Yoga in the Park",
        "description": "Start your Sunday with mindfulness and movement! Join us for a refreshing outdoor yoga session suitable for all levels. We'll practice gentle flows, breathing exercises, and meditation surrounded by nature. Bring your own mat, water bottle, and positive energy. Free community event - donations welcome to support local yoga instructors.",
        "category": "Sports & Fitness",
        "location": "Golden Gate Park, Polo Fields",
        "date_offset": 3,
        "max_participants": 60,
        "latitude": 37.7694,
        "longitude": -122.4862,
        "going_count": 42,
        "interested_count": 28
    },
    {
        "title": "Modern Art Exhibition Opening",
        "description": "Celebrate the opening of 'Urban Perspectives' - a stunning collection of contemporary art from emerging Bay Area artists. Explore paintings, sculptures, and multimedia installations that capture the essence of modern city life. Meet the artists, enjoy complimentary wine and hors d'oeuvres, and be part of San Francisco's vibrant art scene.",
        "category": "Arts & Culture",
        "location": "SF MoMA, 151 3rd St, San Francisco",
        "date_offset": 7,
        "max_participants": 200,
        "latitude": 37.7857,
        "longitude": -122.4011,
        "going_count": 87,
        "interested_count": 134
    },
    {
        "title": "Startup Founders Networking Mixer",
        "description": "Connect with fellow entrepreneurs, investors, and innovators in the Bay Area startup ecosystem. This mixer is designed for early-stage founders looking to build their network, find co-founders, or meet potential investors. Featuring lightning talks from successful founders, 1-on-1 networking sessions, and plenty of time to make meaningful connections. Pizza and drinks provided!",
        "category": "Business & Professional",
        "location": "WeWork SoMa, 600 California St",
        "date_offset": 4,
        "max_participants": 100,
        "latitude": 37.7929,
        "longitude": -122.4058,
        "going_count": 76,
        "interested_count": 42
    },
    {
        "title": "Beach Cleanup & BBQ Social",
        "description": "Make a difference while making new friends! Join our monthly beach cleanup event followed by a community BBQ. We'll provide gloves, bags, and all cleanup supplies. After 2 hours of helping our coastline, we'll fire up the grills for a well-deserved feast. Bring your family, friends, and good vibes. Together we can keep our beaches beautiful!",
        "category": "Community Service",
        "location": "Ocean Beach, Great Highway",
        "date_offset": 6,
        "max_participants": 80,
        "latitude": 37.7594,
        "longitude": -122.5107,
        "going_count": 54,
        "interested_count": 31
    },
    {
        "title": "Gourmet Food Truck Festival",
        "description": "The biggest food truck festival of the year returns! Taste incredible dishes from 40+ of the Bay Area's best food trucks. From authentic tacos to gourmet burgers, vegan delights to decadent desserts - there's something for every palate. Live music all day, craft beer garden, family-friendly activities. Don't miss this delicious celebration!",
        "category": "Food & Drink",
        "location": "Fort Mason Center, 2 Marina Blvd",
        "date_offset": 8,
        "max_participants": 500,
        "latitude": 37.8057,
        "longitude": -122.4318,
        "going_count": 342,
        "interested_count": 189
    },
    {
        "title": "Python Web Development Workshop",
        "description": "Learn to build modern web applications with Python and Flask! This hands-on workshop covers everything from basics to deployment. Topics include: routing, templates, databases, authentication, and RESTful APIs. Perfect for beginners with basic Python knowledge. Bring your laptop with Python 3.9+ installed. All materials and code examples provided.",
        "category": "Education & Learning",
        "location": "General Assembly SF, 225 Bush St",
        "date_offset": 10,
        "max_participants": 30,
        "latitude": 37.7908,
        "longitude": -122.4013,
        "going_count": 28,
        "interested_count": 45
    },
    {
        "title": "5K Fun Run for Local Schools",
        "description": "Lace up your running shoes for a great cause! This 5K fun run benefits local school programs. All fitness levels welcome - walk, jog, or run at your own pace. The scenic route winds through the beautiful Presidio. Every participant receives a t-shirt and finisher medal. Kids under 12 run free! Post-race celebration with music, food, and awards ceremony.",
        "category": "Sports & Fitness",
        "location": "Presidio Main Post, Graham St",
        "date_offset": 9,
        "max_participants": 300,
        "latitude": 37.7989,
        "longitude": -122.4662,
        "going_count": 187,
        "interested_count": 92
    },
    {
        "title": "Live Jazz & Wine Tasting Evening",
        "description": "An elegant evening of smooth jazz and fine wines. Sample premium wines from Napa and Sonoma valleys while enjoying live performances from acclaimed jazz musicians. Includes wine education session with a certified sommelier, gourmet cheese and charcuterie board, and intimate concert setting. Limited seating for an exclusive experience. Must be 21+.",
        "category": "Music",
        "location": "The Fillmore, 1805 Geary Blvd",
        "date_offset": 11,
        "max_participants": 120,
        "latitude": 37.7842,
        "longitude": -122.4331,
        "going_count": 94,
        "interested_count": 67
    },
    {
        "title": "Urban Hiking Adventure: Twin Peaks",
        "description": "Discover San Francisco from its highest point! This moderate-difficulty urban hike takes us up to Twin Peaks for breathtaking 360-degree views of the city, bay, and beyond. Perfect for photography enthusiasts and nature lovers. Wear comfortable shoes, bring water and snacks. We'll make several stops to learn about SF history and ecology. All fitness levels encouraged!",
        "category": "Sports & Fitness",
        "location": "Twin Peaks Summit, Christmas Tree Point Rd",
        "date_offset": 12,
        "max_participants": 40,
        "latitude": 37.7544,
        "longitude": -122.4477,
        "going_count": 32,
        "interested_count": 18
    },
    {
        "title": "Women in Tech: Leadership Panel",
        "description": "Inspiring panel discussion featuring successful women leaders in technology. Hear their stories, challenges, and advice for advancing your career in tech. Topics include: overcoming imposter syndrome, negotiating salary, building your personal brand, and creating inclusive workplaces. Q&A session, networking reception, and mentor matchmaking opportunity. All genders welcome!",
        "category": "Business & Professional",
        "location": "Salesforce Tower, 415 Mission St",
        "date_offset": 14,
        "max_participants": 150,
        "latitude": 37.7897,
        "longitude": -122.3972,
        "going_count": 112,
        "interested_count": 78
    },
    {
        "title": "Craft Beer Brewing Workshop",
        "description": "Ever wanted to brew your own beer? Learn the art and science of craft beer brewing from expert brewers. Hands-on experience covering ingredient selection, brewing process, fermentation, and bottling. Sample different beer styles, take home your own brewing kit, and receive recipes to continue brewing at home. Includes lunch and beer tastings. 21+ only.",
        "category": "Food & Drink",
        "location": "Anchor Brewing Company, 1705 Mariposa St",
        "date_offset": 15,
        "max_participants": 25,
        "latitude": 37.7644,
        "longitude": -122.4015,
        "going_count": 22,
        "interested_count": 34
    },
    {
        "title": "Street Photography Walk: Mission District",
        "description": "Explore the vibrant Mission District through your lens! This guided photography walk focuses on street photography techniques, composition, and capturing authentic moments. Visit colorful murals, bustling streets, and hidden gems. All camera types welcome - DSLR, mirrorless, or smartphone. Suitable for beginners and intermediate photographers. Ends with optional coffee shop photo review session.",
        "category": "Arts & Culture",
        "location": "Mission District, 24th St BART Station",
        "date_offset": 13,
        "max_participants": 20,
        "latitude": 37.7522,
        "longitude": -122.4186,
        "going_count": 16,
        "interested_count": 12
    },
    {
        "title": "Sustainable Living Workshop",
        "description": "Learn practical ways to reduce your environmental footprint and live more sustainably. Topics include: zero-waste strategies, composting basics, eco-friendly products, sustainable fashion, and green energy options. Featuring local sustainability experts, DIY demonstrations, and resource fair. Take home a sustainability starter kit. Free event, but registration required.",
        "category": "Environment",
        "location": "Rainbow Grocery, 1745 Folsom St",
        "date_offset": 16,
        "max_participants": 60,
        "latitude": 37.7681,
        "longitude": -122.4147,
        "going_count": 48,
        "interested_count": 52
    },
    {
        "title": "Salsa Dancing Night: Beginner Friendly",
        "description": "Experience the passion and rhythm of salsa! No partner or experience needed - we'll teach you the basics and have you dancing in no time. Professional instructors lead a beginner lesson from 7-8 PM, followed by social dancing until midnight. Great music, friendly atmosphere, and a welcoming community. First drink included with admission!",
        "category": "Arts & Culture",
        "location": "Cafe Cocomo, 650 Indiana St",
        "date_offset": 17,
        "max_participants": 100,
        "latitude": 37.7619,
        "longitude": -122.3909,
        "going_count": 73,
        "interested_count": 44
    },
    {
        "title": "Full Moon Meditation & Sound Bath",
        "description": "Harness the energy of the full moon with this transformative meditation and sound healing experience. Immerse yourself in soothing vibrations from crystal singing bowls, gongs, and chimes. Perfect for stress relief, deep relaxation, and spiritual connection. Bring a yoga mat, blanket, and pillow. Wear comfortable clothing. All levels welcome, no experience necessary.",
        "category": "Health & Wellness",
        "location": "Yoga Garden SF, 286 Divisadero St",
        "date_offset": 19,
        "max_participants": 35,
        "latitude": 37.7726,
        "longitude": -122.4378,
        "going_count": 32,
        "interested_count": 19
    },
    {
        "title": "Coding Bootcamp Open House",
        "description": "Considering a career in tech? Join us for an open house to learn about our intensive coding bootcamp. Tour our facilities, meet instructors and alumni, attend a sample coding class, and get all your questions answered. Learn about curriculum, job placement rates, financing options, and how to prepare for the bootcamp. Free pizza and Q&A session!",
        "category": "Education & Learning",
        "location": "Hack Reactor SF, 944 Market St",
        "date_offset": 18,
        "max_participants": 80,
        "latitude": 37.7826,
        "longitude": -122.4099,
        "going_count": 56,
        "interested_count": 87
    },
    {
        "title": "Farmers Market & Live Music",
        "description": "Support local farmers and artisans at our weekly farmers market! Fresh organic produce, artisan breads, local honey, handmade crafts, and more. This week featuring live acoustic music from local musicians. Bring your reusable bags and appetite. Kid-friendly activities, food trucks, and community atmosphere. Rain or shine!",
        "category": "Community",
        "location": "Ferry Building Marketplace, Embarcadero",
        "date_offset": 1,  # Tomorrow
        "max_participants": 300,
        "latitude": 37.7956,
        "longitude": -122.3933,
        "going_count": 156,
        "interested_count": 78
    },
    {
        "title": "Improv Comedy Workshop & Show",
        "description": "Laugh your way into improv comedy! Join professional comedians for a 2-hour workshop teaching improv fundamentals - think fast, be bold, and have fun. Learn games like 'Yes And', scene work, and character development. Workshop participants get free admission to the evening improv show. No experience necessary, just bring your sense of humor!",
        "category": "Arts & Culture",
        "location": "BATS Improv, Bayfront Theater, Fort Mason",
        "date_offset": 20,
        "max_participants": 40,
        "latitude": 37.8057,
        "longitude": -122.4318,
        "going_count": 34,
        "interested_count": 21
    },
    {
        "title": "E-Sports Tournament: FIFA 2026",
        "description": "Calling all FIFA gamers! Compete in our monthly tournament for glory and prizes. Open to all skill levels with beginner and advanced brackets. PlayStation 5 setups, live streaming, commentary, and awesome gaming atmosphere. Grand prize: $500 and gaming gear. Spectators welcome! Food and drinks available. Pre-registration required.",
        "category": "Sports & Fitness",
        "location": "GameHaus, 1 Polk St",
        "date_offset": 21,
        "max_participants": 64,
        "latitude": 37.7833,
        "longitude": -122.4190,
        "going_count": 58,
        "interested_count": 23
    },
    {
        "title": "Climate Action Town Hall",
        "description": "Join community leaders, environmental advocates, and concerned citizens for an important discussion on local climate action. Learn about SF's climate goals, proposed green initiatives, and how you can make a difference. Panel discussion with city officials, breakout sessions on specific topics, and opportunities to get involved with local environmental organizations. Your voice matters!",
        "category": "Environment",
        "location": "SF City Hall, 1 Dr Carlton B Goodlett Pl",
        "date_offset": 22,
        "max_participants": 200,
        "latitude": 37.7792,
        "longitude": -122.4191,
        "going_count": 143,
        "interested_count": 98
    },
]

def clear_existing_events():
    """Clear all existing events and RSVPs"""
    try:
        print("🗑️  Clearing existing event RSVPs...")
        supabase.table('event_rsvps').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("🗑️  Clearing existing event comments...")
        supabase.table('event_comments').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("🗑️  Clearing existing saved events...")
        supabase.table('saved_events').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("🗑️  Clearing existing events...")
        supabase.table('events').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("✅ Successfully cleared existing event data\n")
    except Exception as e:
        print(f"❌ Error clearing existing data: {e}\n")

def get_all_users():
    """Fetch all users from database"""
    try:
        response = supabase.table('users').select('id, name').execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []

def seed_events(users):
    """Seed events with realistic data"""
    if len(users) < 5:
        print("❌ Need at least 5 users to seed events properly")
        return
    
    print(f"📅 Creating {len(EVENTS_DATA)} diverse events...\n")
    
    for i, event_data in enumerate(EVENTS_DATA):
        try:
            # Select random organizer
            organizer = random.choice(users)
            
            # Calculate event date
            event_date = datetime.now() + timedelta(days=event_data['date_offset'])
            
            # Create event
            event = {
                'title': event_data['title'],
                'description': event_data['description'],
                'category': event_data['category'],
                'location': event_data['location'],
                'date_time': event_date.isoformat(),
                'max_participants': event_data['max_participants'],
                'organizer_id': organizer['id'],
                'image_url': EVENT_IMAGES[i % len(EVENT_IMAGES)],
                'latitude': event_data.get('latitude'),
                'longitude': event_data.get('longitude')
            }
            
            response = supabase.table('events').insert(event).execute()
            created_event = response.data[0]
            event_id = created_event['id']
            
            print(f"✅ Created: {event_data['title']}")
            print(f"   📍 {event_data['location']}")
            print(f"   📅 {event_date.strftime('%b %d, %Y')}")
            print(f"   👤 Organizer: {organizer['name']}")
            
            # Add RSVPs - Going
            going_count = event_data['going_count']
            interested_count = event_data['interested_count']
            
            # Shuffle users and pick attendees
            shuffled_users = random.sample(users, min(len(users), going_count + interested_count))
            
            rsvp_count = 0
            for j, user in enumerate(shuffled_users[:going_count]):
                if user['id'] != organizer['id']:  # Don't RSVP as organizer
                    try:
                        supabase.table('event_rsvps').insert({
                            'event_id': event_id,
                            'user_id': user['id'],
                            'status': 'going'
                        }).execute()
                        rsvp_count += 1
                    except:
                        pass
            
            # Add RSVPs - Interested
            for j, user in enumerate(shuffled_users[going_count:going_count + interested_count]):
                if user['id'] != organizer['id']:
                    try:
                        supabase.table('event_rsvps').insert({
                            'event_id': event_id,
                            'user_id': user['id'],
                            'status': 'interested'
                        }).execute()
                        rsvp_count += 1
                    except:
                        pass
            
            print(f"   👥 {rsvp_count} RSVPs added")
            
            # Add some comments (20% of events get 2-5 comments)
            if random.random() < 0.2:
                comment_count = random.randint(2, 5)
                comments = [
                    "Can't wait for this event! 🎉",
                    "This looks amazing, see you there!",
                    "Will there be parking available?",
                    "Bringing my friends, this is going to be awesome!",
                    "Perfect timing, I've been looking for something like this!",
                    "Is this beginner-friendly?",
                    "Great lineup of speakers/activities!",
                    "Thanks for organizing this! 🙌",
                ]
                
                for _ in range(min(comment_count, len(shuffled_users))):
                    try:
                        user = random.choice(shuffled_users)
                        comment_text = random.choice(comments)
                        supabase.table('event_comments').insert({
                            'event_id': event_id,
                            'user_id': user['id'],
                            'comment': comment_text
                        }).execute()
                    except:
                        pass
                print(f"   💬 {comment_count} comments added")
            
            print()
            
        except Exception as e:
            print(f"❌ Error creating event '{event_data['title']}': {e}\n")

def main():
    print("=" * 70)
    print("🎯 COMPREHENSIVE EVENT SEEDING SCRIPT")
    print("=" * 70)
    print()
    
    # Get users
    print("👥 Fetching users...")
    users = get_all_users()
    print(f"✅ Found {len(users)} users\n")
    
    if len(users) < 5:
        print("❌ Please run seed_complete.py first to create users!")
        return
    
    # Clear existing events
    clear_existing_events()
    
    # Seed new events
    seed_events(users)
    
    print("=" * 70)
    print("🎉 EVENT SEEDING COMPLETE!")
    print("=" * 70)
    print(f"✅ Created {len(EVENTS_DATA)} diverse events")
    print("✅ Added realistic RSVPs and attendance")
    print("✅ Added sample comments to some events")
    print("✅ All events have proper locations with coordinates")
    print("\n🚀 Visit /events to explore the new events!")

if __name__ == "__main__":
    main()
