#!/usr/bin/env python3
"""
Quick test to verify backend server is running
"""
import requests
import sys

def test_backend():
    try:
        # Test basic connectivity
        response = requests.get('http://localhost:5000/api/dashboard/health', timeout=5)
        print(f"Backend is running! Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("Backend server is not running on localhost:5000")
        return False
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return False

def test_cors():
    try:
        # Test CORS preflight
        response = requests.options('http://localhost:5000/api/funcionarios', 
                                  headers={'Origin': 'http://localhost:3000'}, 
                                  timeout=5)
        print(f"CORS preflight test: {response.status_code}")
        print(f"CORS headers: {dict(response.headers)}")
        return True
    except Exception as e:
        print(f"CORS test failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing Backend Connectivity")
    print("=" * 40)
    
    backend_ok = test_backend()
    if backend_ok:
        test_cors()
    else:
        print("\nTo start the backend server:")
        print("   cd backend")
        print("   python app.py")