#!/usr/bin/env python3
"""
Comprehensive Group Seeding Script
Seeds 15+ diverse, realistic groups with proper members
"""

import os
import sys
import random

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app to get configured supabase client
from app import create_app
from app.utils.supabase_client import supabase_admin as supabase

app = create_app()
app.app_context().push()

# Group images - diverse, high quality
GROUP_IMAGES = [
    "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",  # Team collaboration
    "https://images.unsplash.com/photo-1551632811-561732d1e306?w=400",  # Mountains/hiking
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",  # Portrait/professional
    "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400",  # Minimal interior
    "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400",  # Food
    "https://images.unsplash.com/photo-1511367461989-f85a21fda167?w=400",  # Music/concert
    "https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?w=400",  # Tech/coding
    "https://images.unsplash.com/photo-1535320903710-d993d3d77d29?w=400",  # Fitness/yoga
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",  # Nature/landscape
    "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400",  # Art/creative
    "https://images.unsplash.com/photo-1579547621706-1a9c79d5c9f1?w=400",  # Gaming
    "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400",  # Environment
    "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400",  # Business
    "https://images.unsplash.com/photo-1511882150382-421056c89033?w=400",  # Book club
    "https://images.unsplash.com/photo-1556155092-490a1ba16284?w=400",  # Photography
]

# Comprehensive group data
GROUPS_DATA = [
    {
        "name": "UX Designers Hub",
        "description": "A place to share wireframes, get feedback on your latest prototypes, and discuss user research. We meet monthly for portfolio reviews and design critiques. All experience levels welcome!",
        "category": "Technology",
        "is_private": False,
        "target_members": 45
    },
    {
        "name": "Weekend Hikers SF",
        "description": "Organizing trails around the Bay Area every Sunday morning. Beginners welcome! We explore everything from easy coastal walks to challenging mountain hikes. Carpool coordination and trail recommendations shared weekly.",
        "category": "Sports & Fitness",
        "is_private": False,
        "target_members": 38
    },
    {
        "name": "Minimalist Living",
        "description": "Declutter your life and mind. Tips for sustainable and simple living. Share your journey towards minimalism, discuss decluttering strategies, and find inspiration for intentional living.",
        "category": "Lifestyle",
        "is_private": False,
        "target_members": 52
    },
    {
        "name": "Local Foodies SF",
        "description": "Discovering hidden gems and best eats in the downtown area. Restaurant recommendations, food tours, cooking tips, and occasional group dinners. From hole-in-the-wall taquerias to upscale dining!",
        "category": "Food & Drink",
        "is_private": False,
        "target_members": 67
    },
    {
        "name": "Swift & Kotlin Developers",
        "description": "Technical discussions on native mobile development. Share code snippets, discuss architecture patterns, and help each other with challenging bugs. No cross-platform wars allowed! Monthly code review sessions.",
        "category": "Technology",
        "is_private": False,
        "target_members": 34
    },
    {
        "name": "Climate Action Warriors",
        "description": "Taking real steps towards sustainability. From policy advocacy to community cleanup events, we're making a difference. Join us for beach cleanups, tree planting, and climate town halls. Every action counts!",
        "category": "Environment",
        "is_private": False,
        "target_members": 56
    },
    {
        "name": "Indie Music Lovers",
        "description": "Discover new artists, share playlists, and attend local shows together. From bedroom pop to garage rock, we celebrate independent music. Weekly listening parties and concert meetups!",
        "category": "Arts & Culture",
        "is_private": False,
        "target_members": 43
    },
    {
        "name": "Python Enthusiasts",
        "description": "Whether you're automating tasks, building web apps, or diving into data science - this is your community. Weekly coding challenges, project showcases, and beginner-friendly help.",
        "category": "Technology",
        "is_private": False,
        "target_members": 61
    },
    {
        "name": "Morning Meditation Circle",
        "description": "Start your day with mindfulness. We meet virtually every weekday at 7 AM for guided meditation. All levels welcome. Find peace, reduce stress, and build a consistent practice with supportive community.",
        "category": "Health & Wellness",
        "is_private": False,
        "target_members": 29
    },
    {
        "name": "Startup Founders Network",
        "description": "Early-stage founders supporting each other through the journey. Share challenges, celebrate wins, get feedback on your pitch, find co-founders. Monthly meetups and a supportive Slack channel.",
        "category": "Business & Professional",
        "is_private": True,
        "target_members": 24
    },
    {
        "name": "Street Photography SF",
        "description": "Capture the soul of the city through your lens. Weekly photo walks through different neighborhoods. Share techniques, get feedback, and appreciate the art of candid photography. DSLR or smartphone - all cameras welcome!",
        "category": "Arts & Culture",
        "is_private": False,
        "target_members": 31
    },
    {
        "name": "Board Game Nights",
        "description": "From Catan to Pandemic, we love strategic tabletop games! Biweekly game nights at local cafes. Bring your favorites or try something new. Great for making friends and exercising your brain!",
        "category": "Entertainment",
        "is_private": False,
        "target_members": 48
    },
    {
        "name": "Women in Tech SF",
        "description": "Empowering women in technology careers. Mentorship, job opportunities, speaker events, and a supportive community. From engineers to product managers, designers to data scientists - all tech roles welcome!",
        "category": "Business & Professional",
        "is_private": False,
        "target_members": 73
    },
    {
        "name": "Urban Gardeners",
        "description": "Growing food in small spaces! Share tips on container gardening, balcony herbs, community garden plots, and sustainable urban farming. Seed swaps and garden tours included!",
        "category": "Environment",
        "is_private": False,
        "target_members": 36
    },
    {
        "name": "Book Club: Sci-Fi Edition",
        "description": "Exploring the universe through science fiction. Monthly book picks, thoughtful discussions, and author Q&As. From classic Asimov to modern Liu Cixin. Currently reading 'Project Hail Mary'!",
        "category": "Education & Learning",
        "is_private": False,
        "target_members": 27
    },
    {
        "name": "Salsa Dancing Beginners",
        "description": "Learn salsa in a fun, supportive environment! No partner needed. We meet every Thursday evening for lessons followed by social dancing. Perfect for absolute beginners - we all start somewhere!",
        "category": "Arts & Culture",
        "is_private": False,
        "target_members": 41
    },
    {
        "name": "Remote Work Nomads",
        "description": "Digital nomads and remote workers sharing tips, coworking spaces, and travel recommendations. Discuss productivity hacks, visa requirements, and the best coffee shops with strong WiFi!",
        "category": "Lifestyle",
        "is_private": False,
        "target_members": 54
    },
    {
        "name": "Home Brewers United",
        "description": "Craft your own beer! Share recipes, troubleshoot fermentation issues, and taste each other's brews. From IPAs to stouts, we're passionate about homebrewing. Monthly brew days and competitions!",
        "category": "Food & Drink",
        "is_private": False,
        "target_members": 22
    },
]

def clear_existing_groups():
    """Clear all existing groups and members"""
    try:
        print("🗑️  Clearing existing group members...")
        supabase.table('group_members').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("🗑️  Clearing existing groups...")
        supabase.table('groups').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        print("✅ Successfully cleared existing group data\n")
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

def seed_groups(users):
    """Seed groups with realistic data"""
    if len(users) < 5:
        print("❌ Need at least 5 users to seed groups properly")
        return
    
    print(f"👥 Creating {len(GROUPS_DATA)} diverse groups...\n")
    
    for i, group_data in enumerate(GROUPS_DATA):
        try:
            # Select random creator
            creator = random.choice(users)
            
            # Create group
            group = {
                'name': group_data['name'],
                'description': group_data['description'],
                'category': group_data['category'],
                'is_private': group_data['is_private'],
                'creator_id': creator['id'],
                'image_url': GROUP_IMAGES[i % len(GROUP_IMAGES)]
            }
            
            response = supabase.table('groups').insert(group).execute()
            created_group = response.data[0]
            group_id = created_group['id']
            
            print(f"✅ Created: {group_data['name']}")
            print(f"   📁 {group_data['category']}")
            print(f"   {'🔒' if group_data['is_private'] else '🌐'} {'Private' if group_data['is_private'] else 'Public'}")
            print(f"   👤 Creator: {creator['name']}")
            
            # Add creator as admin (automatically done by model, but verify)
            try:
                supabase.table('group_members').insert({
                    'group_id': group_id,
                    'user_id': creator['id'],
                    'role': 'admin'
                }).execute()
            except:
                pass  # Might already exist from model
            
            # Add members
            target_members = group_data['target_members']
            
            # Shuffle users and pick members (excluding creator)
            potential_members = [u for u in users if u['id'] != creator['id']]
            shuffled_members = random.sample(potential_members, min(len(potential_members), target_members - 1))
            
            member_count = 1  # Creator already counted
            for member in shuffled_members:
                try:
                    # Most are regular members, some are moderators
                    role = 'moderator' if random.random() < 0.1 else 'member'
                    
                    supabase.table('group_members').insert({
                        'group_id': group_id,
                        'user_id': member['id'],
                        'role': role
                    }).execute()
                    member_count += 1
                except:
                    pass
            
            print(f"   👥 {member_count} members added")
            print()
            
        except Exception as e:
            print(f"❌ Error creating group '{group_data['name']}': {e}\n")

def main():
    print("=" * 70)
    print("👥 COMPREHENSIVE GROUP SEEDING SCRIPT")
    print("=" * 70)
    print()
    
    # Get users
    print("👥 Fetching users...")
    users = get_all_users()
    print(f"✅ Found {len(users)} users\n")
    
    if len(users) < 5:
        print("❌ Please run seed_complete.py first to create users!")
        return
    
    # Clear existing groups
    clear_existing_groups()
    
    # Seed new groups
    seed_groups(users)
    
    print("=" * 70)
    print("🎉 GROUP SEEDING COMPLETE!")
    print("=" * 70)
    print(f"✅ Created {len(GROUPS_DATA)} diverse groups")
    print("✅ Added realistic member counts")
    print("✅ Assigned proper roles (admin/moderator/member)")
    print("✅ Mix of public and private groups")
    print("\n🚀 Visit /groups to explore the new groups!")

if __name__ == "__main__":
    main()
