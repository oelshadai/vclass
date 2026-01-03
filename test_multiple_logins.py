#!/usr/bin/env python3
"""
Test multiple student logins
"""
import requests
import json

def test_multiple_students():
    """Test login for multiple students"""
    
    # Test students with their credentials
    students_to_test = [
        {"student_id": "2025BASIC_9004", "password": "8AuoU2", "name": "gideon sarpong"},
        {"student_id": "STD001", "password": "test123", "name": "John Test Doe"},
        {"student_id": "ST001", "password": "HKk5lW", "name": "Kofi Mensah"},
        {"student_id": "ST002", "password": "HZLPXO", "name": "Ama Boateng"}
    ]
    
    api_url = "http://localhost:8000/api/students/auth/login/"
    
    for student_data in students_to_test:
        print(f"\n=== Testing {student_data['name']} ===")
        payload = {
            "student_id": student_data["student_id"],
            "password": student_data["password"]
        }
        
        try:
            response = requests.post(api_url, json=payload, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[SUCCESS] Login successful for {student_data['name']}")
                print(f"  Student ID: {data['student']['student_id']}")
                print(f"  Class: {data['student']['class']}")
                print(f"  Username: {data['student']['username']}")
            else:
                print(f"[ERROR] Login failed for {student_data['name']}")
                try:
                    error_data = response.json()
                    print(f"  Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"  Raw error: {response.text}")
                    
        except Exception as e:
            print(f"[ERROR] Exception for {student_data['name']}: {e}")

if __name__ == "__main__":
    test_multiple_students()