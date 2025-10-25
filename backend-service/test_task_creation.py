#!/usr/bin/env python3
"""
Test task creation specifically
"""

def test_task_creation():
    """Test task creation with proper authentication"""
    base_url = "http://localhost:8000"
    
    print("Testing Task Creation...")
    print("=" * 40)
    
    # Step 1: Create a new user
    print("\n1. Creating new user...")
    signup_data = {
        "username": "taskuser",
        "email": "taskuser@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("[OK] User created successfully")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
        else:
            print(f"[ERROR] User creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] User creation failed: {e}")
        return False
    
    # Step 2: Login to get token
    print("\n2. Logging in...")
    login_data = {
        "username": "taskuser",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("[OK] Login successful")
            token_data = response.json()
            access_token = token_data['access_token']
        else:
            print(f"[ERROR] Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return False
    
    # Step 3: Create task
    print("\n3. Creating task...")
    task_data = {
        "title": "Test Task Creation",
        "description": "Testing task creation with proper authentication",
        "status": "pending",
        "priority": "high"
    }
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{base_url}/api/tasks",
            json=task_data,
            headers=headers
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("[OK] Task created successfully")
            task = response.json()
            print(f"   Task ID: {task['id']}")
            print(f"   Title: {task['title']}")
            print(f"   Status: {task['status']}")
            print(f"   Assigned User ID: {task['assigned_user_id']}")
        else:
            print(f"[ERROR] Task creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Task creation failed: {e}")
        return False
    
    print("\n[SUCCESS] Task creation test completed!")
    return True

if __name__ == "__main__":
    test_task_creation()
