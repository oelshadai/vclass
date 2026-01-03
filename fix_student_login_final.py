#!/usr/bin/env python3
"""
Final Student Login Fix Script
Diagnoses and fixes the core issue: password synchronization between Student and User models
"""
import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

from students.models import Student
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def diagnose_student_login(student_id):
    """Comprehensive diagnosis of student login issues"""
    print(f"\n=== DIAGNOSING STUDENT LOGIN: {student_id} ===")
    
    try:
        student = Student.objects.get(student_id=student_id)
        print(f"✓ Student found: {student.get_full_name()}")
        print(f"  Student ID: {student.student_id}")
        print(f"  Username: {student.username}")
        print(f"  Plain password: {student.password}")
        
        if not student.user:
            print("✗ CRITICAL: No User account linked to student")
            return False, "NO_USER_ACCOUNT"
        
        print(f"  User ID: {student.user.id}")
        print(f"  User email: {student.user.email}")
        print(f"  User is_active: {student.user.is_active}")
        
        # Test password verification
        if student.password:
            password_works = student.user.check_password(student.password)
            print(f"  Password verification: {'✓ WORKS' if password_works else '✗ FAILS'}")
            
            if not password_works:
                return False, "PASSWORD_MISMATCH"
        else:
            print("✗ CRITICAL: No password set for student")
            return False, "NO_PASSWORD"
        
        # Test authentication methods
        auth_methods = [
            ("Email", student.user.email),
            ("Username", student.username),
            ("Student ID", student_id)
        ]
        
        auth_success = False
        for method, identifier in auth_methods:
            if identifier:
                user = authenticate(username=identifier, password=student.password)
                success = user is not None
                print(f"  Auth via {method}: {'✓ SUCCESS' if success else '✗ FAILED'}")
                if success:
                    auth_success = True
        
        if auth_success:
            print("✓ LOGIN SHOULD WORK")
            return True, "SUCCESS"
        else:
            return False, "AUTH_FAILED"
            
    except Student.DoesNotExist:
        print(f"✗ Student {student_id} not found in database")
        return False, "STUDENT_NOT_FOUND"
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False, f"ERROR: {e}"

def fix_student_login(student_id):
    """Fix student login by synchronizing passwords"""
    print(f"\n=== FIXING STUDENT LOGIN: {student_id} ===")
    
    try:
        student = Student.objects.get(student_id=student_id)
        
        if not student.user:
            print("Creating User account for student...")
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            # Create email
            school_domain = student.school.name.lower().replace(' ', '').replace('-', '') if student.school else 'school'
            email = f"{student.username}@{school_domain}.edu"
            
            user = User.objects.create_user(
                email=email,
                password=student.password or 'temp123',
                first_name=student.first_name,
                last_name=student.last_name
            )
            
            if hasattr(user, 'role'):
                user.role = 'STUDENT'
            if hasattr(user, 'school') and student.school:
                user.school = student.school
            user.save()
            
            student.user = user
            student.save()
            print(f"✓ Created User account with email: {email}")
        
        # Ensure password is set
        if not student.password:
            student.password = student.generate_password()
            student.save()
            print(f"✓ Generated new password: {student.password}")
        
        # Sync password to User model
        student.user.set_password(student.password)
        student.user.is_active = True
        student.user.save()
        print(f"✓ Synchronized password to User model")
        
        # Verify fix
        user = authenticate(username=student.user.email, password=student.password)
        if user:
            print(f"✓ LOGIN FIX SUCCESSFUL - Student can now login")
            return True
        else:
            print(f"✗ LOGIN FIX FAILED - Authentication still not working")
            return False
            
    except Exception as e:
        print(f"✗ Error fixing login: {e}")
        return False

def fix_all_students():
    """Fix login for all students with issues"""
    print(f"\n=== FIXING ALL STUDENTS ===")
    
    students = Student.objects.all()
    fixed_count = 0
    issues_found = 0
    
    for student in students:
        success, issue = diagnose_student_login(student.student_id)
        if not success:
            issues_found += 1
            print(f"Issue found for {student.student_id}: {issue}")
            
            if fix_student_login(student.student_id):
                fixed_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Total students: {students.count()}")
    print(f"Issues found: {issues_found}")
    print(f"Successfully fixed: {fixed_count}")

def test_login_endpoint(student_id, password):
    """Test the actual login endpoint logic"""
    print(f"\n=== TESTING LOGIN ENDPOINT: {student_id} ===")
    
    try:
        student = Student.objects.get(student_id=student_id)
        
        if not student.user:
            print("✗ Student account not properly configured")
            return False
        
        # Test authentication methods in order (matching auth_views.py)
        user = None
        
        # Method 1: Django authentication with user's email
        if student.user.email:
            user = authenticate(username=student.user.email, password=password)
            print(f"Method 1 (email): {'✓ SUCCESS' if user else '✗ FAILED'}")
        
        # Method 2: Django authentication with student username
        if not user and hasattr(student, 'username') and student.username:
            user = authenticate(username=student.username, password=password)
            print(f"Method 2 (username): {'✓ SUCCESS' if user else '✗ FAILED'}")
        
        # Method 3: Check if user password matches
        if not user and hasattr(student, 'password') and student.password:
            if student.password == password:
                user = student.user
                print(f"Method 3a (plain text): ✓ SUCCESS")
            elif student.user.check_password(password):
                user = student.user
                print(f"Method 3b (hashed): ✓ SUCCESS")
            else:
                print(f"Method 3 (password check): ✗ FAILED")
        
        # Method 4: Direct user authentication with student_id
        if not user:
            user = authenticate(username=student_id, password=password)
            print(f"Method 4 (student_id): {'✓ SUCCESS' if user else '✗ FAILED'}")
        
        if user:
            print(f"✓ LOGIN ENDPOINT WOULD SUCCEED")
            return True
        else:
            print(f"✗ LOGIN ENDPOINT WOULD FAIL")
            return False
            
    except Student.DoesNotExist:
        print(f"✗ Student not found")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== STUDENT LOGIN DIAGNOSTIC & FIX TOOL ===")
    
    # Test with a specific student if available
    test_students = [
        ("2025BASIC_9004", "8AuoU2"),
        ("TEST001", "test123")
    ]
    
    for student_id, password in test_students:
        if Student.objects.filter(student_id=student_id).exists():
            print(f"\n{'='*50}")
            print(f"TESTING STUDENT: {student_id}")
            print(f"{'='*50}")
            
            # Diagnose
            success, issue = diagnose_student_login(student_id)
            
            # Fix if needed
            if not success:
                print(f"\nIssue detected: {issue}")
                fix_student_login(student_id)
                
                # Re-test after fix
                print(f"\nRe-testing after fix...")
                diagnose_student_login(student_id)
            
            # Test endpoint logic
            test_login_endpoint(student_id, password)
    
    # Ask user if they want to fix all students
    print(f"\n{'='*50}")
    response = input("Fix all students with login issues? (y/N): ").lower()
    if response == 'y':
        fix_all_students()
    
    print(f"\n=== DIAGNOSTIC COMPLETE ===")
    print("Students should now be able to login with their credentials.")
    print("If issues persist, check:")
    print("1. Frontend is sending correct student_id and password")
    print("2. Backend authentication endpoint is receiving the data")
    print("3. Database connectivity")