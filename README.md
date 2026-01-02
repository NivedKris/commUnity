# CommUnity - Community Engagement Platform

A Flask-based web application that connects citizens with local events, groups, and civic issues.

## 🚀 Features

- **Firebase Authentication**: Email and phone number (OTP) authentication
- **Event Discovery**: Browse and RSVP to local community events
- **Groups & Communities**: Join interest-based groups
- **Issue Reporting**: Report local issues with photos and location
- **Real-time Chat**: Communicate with community members
- **Gamification**: Reputation points and badges for active participation

## 🛠️ Tech Stack

- **Backend**: Flask 3.0
- **Authentication**: Firebase Auth (Email & Phone)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Jinja2 templates with Tailwind CSS
- **Icons**: Material Symbols

## 📋 Prerequisites

- Python 3.9+
- Firebase project with Auth enabled
- Supabase project

## 🔧 Setup Instructions

### 1. Clone and Navigate
```bash
cd /home/turing/community
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Your `.env` file is already configured with:
- Firebase credentials
- Supabase credentials
- Flask secret key

### 5. Setup Supabase Database
1. Go to your Supabase project
2. Navigate to SQL Editor
3. Copy and paste the contents of `database_schema.sql`
4. Execute the SQL script

### 6. Enable Firebase Authentication
In Firebase Console:
1. Go to Authentication → Sign-in method
2. Enable **Email/Password**
3. Enable **Phone** authentication
4. **IMPORTANT**: Go to Authentication → Settings → Authorized domains
5. Add `127.0.0.1` and `localhost` to the authorized domains list
   - Without this, phone authentication will fail with OAuth error

### 7. Run the Application
```bash
python run.py
```

The app will be available at: `http://localhost:5000`

## 📁 Project Structure

```
community/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration
│   ├── models.py             # User model
│   ├── routes/               # Route blueprints
│   │   ├── main.py           # Landing & dashboard
│   │   ├── auth.py           # Authentication
│   │   ├── events.py         # Events
│   │   ├── groups.py         # Groups
│   │   ├── issues.py         # Issue reporting
│   │   └── chat.py           # Messaging
│   ├── templates/            # Jinja2 templates
│   ├── static/               # Static files
│   └── utils/                # Utilities
│       ├── firebase_client.py
│       ├── supabase_client.py
│       └── decorators.py
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── database_schema.sql       # Database schema
└── run.py                    # Application entry point
```

## 🔐 Authentication Flow

1. **Email/Password**: 
   - User signs up/logs in with email
   - Firebase creates user
   - Backend verifies token and creates Supabase user record

2. **Phone (OTP)**:
   - User enters phone number
   - Firebase sends OTP via SMS
   - User verifies OTP
   - Backend creates/fetches Supabase user record

## 🌐 Routes

- `/` - Landing page
- `/auth/login` - Login page (email or phone)
- `/auth/signup` - Signup page
- `/auth/logout` - Logout
- `/dashboard` - User dashboard
- `/events` - Events listing (coming soon)
- `/groups` - Groups listing (coming soon)
- `/issues` - Issues listing (coming soon)
- `/chat` - Chat interface (coming soon)

## 🔜 Next Steps (Phase 2+)

- [ ] Implement events CRUD
- [ ] Implement groups CRUD
- [ ] Implement issue reporting
- [ ] Add real-time chat with Supabase Realtime
- [ ] Implement search and filters
- [ ] Add map integration (Google Maps/Leaflet)
- [ ] Implement notification system
- [ ] Add reputation/points system
- [ ] Create admin panel

## 📝 Notes

- The app uses Firebase for authentication only
- All user data and app data is stored in Supabase
- Templates are mobile-first responsive design
- Dark mode support included

## 🐛 Troubleshooting

**Firebase initialization error**: Make sure the Firebase Admin SDK JSON file path in `.env` is correct

**Supabase connection error**: Verify your Supabase URL and keys in `.env`

**Port already in use**: Change the port in `run.py` or kill the process using port 5000

## 📄 License

This project is for educational purposes.
