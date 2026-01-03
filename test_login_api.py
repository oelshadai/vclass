#!/usr/bin/env python3
"""
Test student login API endpoint
"""
import requests
import json

def test_student_login():
    """Test student login via API"""
    
    # Test with the student you mentioned
    api_url = "http://localhost:8000/api/students/auth/login/"
    payload = {
        "student_id": "2025BASIC_9004",  # gideon sarpong
        "password": "8AuoU2"
    }
    
    print(f"Testing API endpoint: {api_url}")
    print(f"Payload: {payload}")
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n[SUCCESS] Login successful!")
            print(f"Access token: {data.get('access', 'Not found')[:50]}...")
            print(f"Student data: {data.get('student', 'Not found')}")
            print(f"Assignments: {len(data.get('assignments', []))} found")
            print(f"Stats: {data.get('stats', 'Not found')}")
        else:
            print("\n[ERROR] Login failed!")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to backend server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"[ERROR] Error testing API: {e}")

if __name__ == "__main__":
    test_student_login()