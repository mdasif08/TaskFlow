#!/usr/bin/env python3
"""
Complete application test for ProjectPulse
Tests the entire flow from signup to task management
"""
import requests

def test_backend_health(base_url):
    """Test backend health endpoint"""
    print("\n1. Testing Backend Health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("[OK] Backend is healthy")
            return True
        else:
            print("[ERROR] Backend health check failed")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Backend not accessible: {e}")
        return False

def test_user_signup(base_url):
    """Test user signup functionality"""
    print("\n2. Testing User Signup...")
    signup_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("[OK] User signup successful")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Username: {user_data['username']}")
            return user_data
        else:
            print(f"[ERROR] Signup failed: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] Signup test failed: {e}")
        return None

def test_user_login(base_url):
    """Test user login functionality"""
    print("\n3. Testing User Login...")
    login_data = {
        "username": "testuser123",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            print("[OK] User login successful")
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"   Token type: {token_data['token_type']}")
            return access_token
        else:
            print(f"[ERROR] Login failed: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"[ERROR] Login test failed: {e}")
        return None

def test_user_profile(base_url, access_token):
    """Test user profile retrieval"""
    print("\n4. Testing User Profile...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{base_url}/api/users/me", headers=headers, timeout=10)
        if response.status_code == 200:
            print("[OK] User profile retrieved")
            profile = response.json()
            print(f"   Username: {profile['username']}")
            print(f"   Email: {profile['email']}")
            return True
        else:
            print(f"[ERROR] Profile retrieval failed: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Profile test failed: {e}")
        return False

def test_task_creation(base_url, access_token, _user_data):
    """Test task creation functionality"""
    print("\n5. Testing Task Creation...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{base_url}/api/tasks",
            json=task_data,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("[OK] Task created successfully")
            task = response.json()
            print(f"   Task ID: {task['id']}")
            print(f"   Title: {task['title']}")
            print(f"   Status: {task['status']}")
            return True
        else:
            print(f"[ERROR] Task creation failed: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Task creation test failed: {e}")
        return False

def test_task_retrieval(base_url, access_token):
    """Test task retrieval functionality"""
    print("\n6. Testing Task Retrieval...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{base_url}/api/tasks", headers=headers, timeout=10)
        if response.status_code == 200:
            print("[OK] Tasks retrieved successfully")
            tasks_data = response.json()
            print(f"   Total tasks: {tasks_data['total']}")
            print(f"   Tasks returned: {len(tasks_data['tasks'])}")
            return True
        else:
            print(f"[ERROR] Task retrieval failed: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Task retrieval test failed: {e}")
        return False

def test_frontend_accessibility(frontend_url):
    """Test frontend accessibility"""
    print("\n7. Testing Frontend Accessibility...")
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("[OK] Frontend is accessible")
        else:
            print(f"[WARNING] Frontend returned status: {response.status_code}")
    except requests.RequestException as e:
        print(f"[WARNING] Frontend not accessible: {e}")
        print("   (This is expected if frontend is not running)")

def print_success_message():
    """Print success message and next steps"""
    print("\n[SUCCESS] All Backend Tests Passed!")
    print("=" * 50)
    print("[OK] ProjectPulse Backend is fully functional!")
    print("[OK] Authentication system working")
    print("[OK] Task management system working")
    print("[OK] Database operations working")
    print("\n[INFO] Next Steps:")
    print("1. Open http://localhost:3001 in your browser")
    print("2. Try signing up with a new account")
    print("3. Create and manage tasks")

def test_full_application():
    """Test the complete ProjectPulse application flow"""
    base_url = "http://localhost:8000"
    frontend_url = "http://localhost:3001"
    
    print("ProjectPulse Full Application Test")
    print("=" * 50)
    
    # Run all tests
    if not test_backend_health(base_url):
        return False
    
    user_data = test_user_signup(base_url)
    if not user_data:
        return False
    
    access_token = test_user_login(base_url)
    if not access_token:
        return False
    
    if not test_user_profile(base_url, access_token):
        return False
    
    if not test_task_creation(base_url, access_token, user_data):
        return False
    
    if not test_task_retrieval(base_url, access_token):
        return False
    
    test_frontend_accessibility(frontend_url)
    print_success_message()
    
    return True

if __name__ == "__main__":
    test_full_application()
