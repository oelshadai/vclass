#!/usr/bin/env python3
"""
Test student login endpoint
"""
import os
import sys
import django
import requests
import json

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

def test_student_login():
    # Test data
    student_id = "2025BASIC_9004"
    password = "8AuoU2"
    
    # API endpoint
    url = "http://localhost:8000/api/auth/student-login/"
    
    # Request payload
    payload = {
        "student_id": student_id,
        "password": password
    }
    
    print(f"Testing student login...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Login successful!")
            print(f"Access Token: {data.get('access', 'Not provided')[:50]}...")
            print(f"User: {data.get('user', {})}")
        else:
            print(f"\n❌ Login failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Raw error: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot connect to Django server")
        print("Make sure Django is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Server took too long to respond")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_student_login()