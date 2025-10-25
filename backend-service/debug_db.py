#!/usr/bin/env python3
"""
Debug database connection and models
"""
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_database():
    """Test database connection and model creation"""
    try:
        print("Testing database connection...")
        
        
        # Test database connection
        print("Creating database session...")
        db = SessionLocal()
        
        # Test creating a user
        print("Testing user creation...")
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("123456")
        )
        
        print("Adding user to database...")
        db.add(test_user)
        db.commit()
        print("User created successfully!")
        
        # Test querying the user
        print("Querying user from database...")
        user = db.query(User).filter(User.username == "testuser").first()
        if user:
            print(f"Found user: {user.username}, {user.email}")
        else:
            print("User not found!")
        
        # Clean up
        print("Cleaning up test data...")
        db.delete(test_user)
        db.commit()
        print("Test data cleaned up!")
        
        db.close()
        print("Database test completed successfully!")
        
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database()
