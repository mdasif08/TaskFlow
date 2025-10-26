#!/usr/bin/env python3
"""
Test connection between frontend and backend
"""
import requests
import time

def test_backend_connection():
    """Test if backend is accessible"""
    print("Testing backend connection...")
    
    # Test localhost
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Localhost backend: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Localhost backend failed: {e}")
    
    # Test network IP
    try:
        response = requests.get("http://192.168.29.92:8000/health", timeout=5)
        print(f"✅ Network IP backend: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Network IP backend failed: {e}")

def test_api_endpoints():
    """Test API endpoints"""
    print("\nTesting API endpoints...")
    
    base_urls = ["http://localhost:8000", "http://192.168.29.92:8000"]
    
    for base_url in base_urls:
        print(f"\nTesting {base_url}:")
        
        # Test root endpoint
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            print(f"  Root: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"  Root: ❌ {e}")
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print(f"  Health: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"  Health: ❌ {e}")
        
        # Test API root
        try:
            response = requests.get(f"{base_url}/api", timeout=5)
            print(f"  API: {response.status_code}")
        except Exception as e:
            print(f"  API: ❌ {e}")

if __name__ == "__main__":
    test_backend_connection()
    test_api_endpoints()
