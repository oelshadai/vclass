#!/usr/bin/env python3
"""
Test student login API directly
"""
import requests
import json

# Test the student login API
def test_student_login():
    url = "http://localhost:8000/api/students/auth/login/"
    
    # Test data
    test_cases = [
        {"student_id": "STD001", "password": "test123"},
        {"student_id": "ST001", "password": "HKk5lW"},
        {"student_id": "ST002", "password": "HZLPXO"}
    ]
    
    for i, credentials in enumerate(test_cases, 1):
        print(f"\n=== Test Case {i} ===")
        print(f"Testing: {credentials}")
        
        try:
            response = requests.post(url, json=credentials)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                print("✅ LOGIN SUCCESS!")
                break
            else:
                print("❌ LOGIN FAILED")
                
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR - Is the backend server running?")
            break
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_student_login()