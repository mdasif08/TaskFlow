#!/usr/bin/env python3
"""
Test script to debug API issues
"""

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing ProjectPulse API...")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"[OK] Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"[OK] Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Root endpoint failed: {e}")
        return
    
    # Test signup endpoint
    try:
        signup_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456"
        }
        response = requests.post(
            f"{base_url}/api/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"[INFO] Signup test: {response.status_code}")
        if response.status_code == 200:
            print(f"[OK] Signup successful: {response.json()}")
        else:
            print(f"[ERROR] Signup failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Signup test failed: {e}")

if __name__ == "__main__":
    test_api()
