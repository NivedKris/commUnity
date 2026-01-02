#!/usr/bin/env python3
"""
Run SQL migrations on Supabase
"""

import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.supabase_client import get_supabase_admin

def run_sql_file(filename):
    """Run SQL from file"""
    supabase = get_supabase_admin()
    
    with open(filename, 'r') as f:
        sql = f.read()
    
    # Split by semicolon and execute each statement
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    for i, statement in enumerate(statements, 1):
        try:
            print(f"Executing statement {i}/{len(statements)}...")
            # Use rpc to execute raw SQL
            result = supabase.rpc('exec_sql', {'sql': statement}).execute()
            print(f"✓ Statement {i} executed successfully")
        except Exception as e:
            # Try direct execution
            try:
                supabase.postgrest.rpc('exec_sql', {'sql': statement}).execute()
                print(f"✓ Statement {i} executed successfully")
            except Exception as e2:
                print(f"⚠ Statement {i} may have failed: {e2}")
                # Continue anyway as some statements might already exist
    
    print(f"\n✅ Finished running {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'add_group_posts_tables.sql'
    
    print(f"Running SQL file: {filename}")
    print("=" * 50)
    run_sql_file(filename)
