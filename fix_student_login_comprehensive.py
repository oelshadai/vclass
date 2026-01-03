#!/usr/bin/env python3
"""
Comprehensive Student Login Fix Script
Fixes password synchronization between Student and User models
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

def test_student_login(student_id, password):
    """Test student login with exact backend logic"""
    print(f"\n=== Testing Login for {student_id} ===")
    
    try:
        student = Student.objects.get(student_id=student_id)
        print(f"✓ Student found: {student.get_full_name()}")
        print(f"  - Student password: {student.password}")
        print(f"  - Username: {student.username}")
        
        if not student.user:
            print("✗ No user account linked")
            return False
            
        print(f"  - User email: {student.user.email}")
        
        # Test all authentication methods
        methods = [
            ("Email auth", student.user.email),
            ("Username auth", student.username),
            ("Student ID auth", student_id)
        ]
        
        for method_name, username in methods:
            if username:
                user = authenticate(username=username, password=password)
                print(f"  {method_name}: {'✓ SUCCESS' if user else '✗ FAILED'}")
                if user:
                    return True
        
        # Test password matching
        if student.password == password:
            print(f"  Plain text match: ✓ SUCCESS")
            return True
        
        if student.user.check_password(password):
            print(f"  Hashed password check: ✓ SUCCESS")
            return True
            
        print("✗ All authentication methods failed")
        return False
        
    except Student.DoesNotExist:
        print(f"✗ Student {student_id} not found")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def fix_student_password(student_id):
    """Fix student password synchronization"""
    try:
        student = Student.objects.get(student_id=student_id)
        
        if not student.user:
            print(f"✗ Student {student_id} has no user account")
            return False
            
        # Sync password from student to user
        if student.password:
            student.user.set_password(student.password)
            student.user.save()
            print(f"✓ Synced password for {student.get_full_name()}")
            return True
        else:
            print(f"✗ Student has no password set")
            return False
            
    except Student.DoesNotExist:
        print(f"✗ Student {student_id} not found")
        return False
    except Exception as e:
        print(f"✗ Error fixing password: {e}")
        return False

def fix_all_students():
    """Fix password sync for all students"""
    students = Student.objects.filter(user__isnull=False, password__isnull=False)
    fixed_count = 0
    
    print(f"\n=== Fixing {students.count()} students ===")
    
    for student in students:
        try:
            if student.password:
                student.user.set_password(student.password)
                student.user.save()
                fixed_count += 1
                print(f"✓ Fixed {student.student_id} - {student.get_full_name()}")
        except Exception as e:
            print(f"✗ Failed to fix {student.student_id}: {e}")
    
    print(f"\n✓ Fixed {fixed_count} students")
    return fixed_count

def create_test_student():
    """Create a test student for verification"""
    from schools.models import School, Class
    
    try:
        # Get first school and class
        school = School.objects.first()
        if not school:
            print("✗ No school found")
            return None
            
        student_class = Class.objects.filter(school=school).first()
        
        # Create test student
        student = Student.objects.create(
            school=school,
            student_id="TEST001",
            first_name="Test",
            last_name="Student",
            gender="M",
            date_of_birth="2010-01-01",
            current_class=student_class,
            guardian_name="Test Guardian",
            guardian_phone="1234567890",
            guardian_address="Test Address",
            admission_date="2024-01-01",
            password="test123"
        )
        
        print(f"✓ Created test student: {student.student_id}")
        return student
        
    except Exception as e:
        print(f"✗ Error creating test student: {e}")
        return None

if __name__ == "__main__":
    print("=== Student Login Fix Script ===")
    
    # Test specific student if exists
    test_student_id = "2025BASIC_9004"
    test_password = "8AuoU2"
    
    print(f"\n1. Testing existing student: {test_student_id}")
    if not test_student_login(test_student_id, test_password):
        print(f"\n2. Fixing password for {test_student_id}")
        if fix_student_password(test_student_id):
            print(f"\n3. Re-testing after fix")
            test_student_login(test_student_id, test_password)
    
    # Fix all students
    print(f"\n4. Fixing all students")
    fix_all_students()
    
    # Create and test new student
    print(f"\n5. Creating test student")
    test_student = create_test_student()
    if test_student:
        test_student_login("TEST001", "test123")
    
    print(f"\n=== Fix Complete ===")