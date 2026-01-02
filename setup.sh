#!/bin/bash

# CommUnity App - Setup Script

echo "🚀 Setting up CommUnity App..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure your .env file is configured"
echo "2. Run the database schema in Supabase SQL Editor (database_schema.sql)"
echo "3. Enable Email and Phone authentication in Firebase Console"
echo "4. Run the app: python run.py"
echo ""
echo "🌐 The app will be available at: http://localhost:5000"
