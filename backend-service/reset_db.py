#!/usr/bin/env python3
"""
Database reset script for ProjectPulse
This script will delete the existing database and recreate it with fresh tables
"""
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))


def reset_database():
    """Reset the database by dropping all tables and recreating them"""
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        
        print("Database reset completed successfully!")
        print("Database file: projectpulse.db")
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("ProjectPulse Database Reset")
    print("=" * 40)
    
    # Check if database file exists
    db_file = Path("projectpulse.db")
    if db_file.exists():
        print(f"Found existing database: {db_file}")
        response = input("This will delete all data. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    reset_database()
