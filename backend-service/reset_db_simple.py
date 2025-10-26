#!/usr/bin/env python3
"""
Simple database reset script for TaskFlow
"""
import os
import sys

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
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()
