#!/usr/bin/env python3
"""
Simple API test script to verify endpoints are working
"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health_endpoints():
    """Test health check endpoints"""
    print("Testing health endpoints...")
    
    # Test dashboard health
    try:
        response = requests.get(f'{BASE_URL}/dashboard/health')
        print(f"Dashboard health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Dashboard health error: {e}")
    
    # Test funcionarios health
    try:
        response = requests.get(f'{BASE_URL}/funcionarios/health')
        print(f"Funcionarios health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Funcionarios health error: {e}")

def test_login():
    """Test login endpoint"""
    print("\nTesting login...")
    
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Token received: {data.get('access_token')[:20]}...")
            return data.get('access_token')
        else:
            print(f"Login error: {response.json()}")
    except Exception as e:
        print(f"Login error: {e}")
    
    return None

def test_authenticated_endpoints(token):
    """Test authenticated endpoints"""
    if not token:
        print("No token available, skipping authenticated tests")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\nTesting authenticated endpoints...")
    
    # Test funcionarios
    try:
        response = requests.get(f'{BASE_URL}/funcionarios/', headers=headers)
        print(f"Funcionarios: {response.status_code}")
        if response.status_code == 200:
            print(f"Found {len(response.json())} funcionarios")
        else:
            print(f"Funcionarios error: {response.json()}")
    except Exception as e:
        print(f"Funcionarios error: {e}")
    
    # Test dashboard resumo
    try:
        response = requests.get(f'{BASE_URL}/dashboard/resumo', headers=headers)
        print(f"Dashboard resumo: {response.status_code}")
        if response.status_code == 200:
            print(f"Dashboard data: {response.json()}")
        else:
            print(f"Dashboard error: {response.json()}")
    except Exception as e:
        print(f"Dashboard error: {e}")

if __name__ == '__main__':
    print("🧪 Testing LashManager API")
    print("=" * 40)
    
    test_health_endpoints()
    token = test_login()
    test_authenticated_endpoints(token)
    
    print("\n✅ API test completed!")