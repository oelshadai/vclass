#!/usr/bin/env python3
import os
import sys
import django

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

from students.models import Student
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def test_student_login(student_id, password):
    """Test student login with the exact same logic as the backend"""
    print(f"Testing login for student_id: {student_id}")
    print(f"Password: {password}")
    print("-" * 50)
    
    try:
        # Find student by student_id
        student = Student.objects.get(student_id=student_id)
        print(f"✓ Student found: {student.get_full_name()}")
        
        # Check if student has a user account
        if not student.user:
            print("✗ Student account not properly configured")
            return False
        
        print(f"✓ Student has user account: {student.user.email}")
        
        # Try authentication methods in order of preference
        user = None
        
        # Method 1: Django authentication with user's email
        if student.user.email:
            user = authenticate(username=student.user.email, password=password)
            print(f"Method 1 (email auth): {'SUCCESS' if user else 'FAILED'}")
        
        # Method 2: Django authentication with student username
        if not user and hasattr(student, 'username') and student.username:
            user = authenticate(username=student.username, password=password)
            print(f"Method 2 (username auth): {'SUCCESS' if user else 'FAILED'}")
        
        # Method 3: Check if user password matches (fallback for plain text passwords)
        if not user and hasattr(student, 'password') and student.password:
            if student.password == password:
                user = student.user
                print(f"Method 3a (plain text match): SUCCESS")
            # Also try checking if the user's password matches
            elif student.user.check_password(password):
                user = student.user
                print(f"Method 3b (hashed password check): SUCCESS")
            else:
                print(f"Method 3 (password check): FAILED")
        
        # Method 4: Direct user authentication with student_id as username
        if not user:
            user = authenticate(username=student_id, password=password)
            print(f"Method 4 (student_id auth): {'SUCCESS' if user else 'FAILED'}")
        
        if user:
            print(f"✓ LOGIN SUCCESS for {student.get_full_name()}")
            return True
        else:
            print(f"✗ LOGIN FAILED - No authentication method worked")
            return False
            
    except Student.DoesNotExist:
        print(f"✗ Student with ID '{student_id}' not found")
        return False
    except Exception as e:
        print(f"✗ Error during login: {str(e)}")
        return False

def fix_student_password(student_id, new_password):
    """Fix student password by updating both student and user records"""
    try:
        student = Student.objects.get(student_id=student_id)
        
        # Update student password (plain text for display)
        student.password = new_password
        student.save()
        
        # Update user password (hashed)
        if student.user:
            student.user.set_password(new_password)
            student.user.save()
            print(f"✓ Password updated for {student.get_full_name()}")
            return True
        else:
            print(f"✗ No user account found for student")
            return False
            
    except Student.DoesNotExist:
        print(f"✗ Student with ID '{student_id}' not found")
        return False
    except Exception as e:
        print(f"✗ Error updating password: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the problematic student
    student_id = "2025BASIC_9004"
    password = "8AuoU2"
    
    print("=== TESTING CURRENT LOGIN ===")
    success = test_student_login(student_id, password)
    
    if not success:
        print("\n=== FIXING PASSWORD ===")
        fix_student_password(student_id, password)
        
        print("\n=== TESTING AFTER FIX ===")
        test_student_login(student_id, password)