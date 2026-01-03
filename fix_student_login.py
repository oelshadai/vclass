#!/usr/bin/env python3
"""
Fix student login issues by ensuring proper user accounts and passwords
"""
import os
import sys
import django

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import Student

def fix_student_login():
    """Fix student login by ensuring proper user accounts"""
    
    print("🔧 Fixing student login issues...")
    
    # Get all students
    students = Student.objects.all()
    
    if not students.exists():
        print("❌ No students found in the database.")
        print("💡 Create a test student first using create_test_student.py")
        return
    
    fixed_count = 0
    
    for student in students:
        print(f"\n👤 Processing student: {student.get_full_name()} (ID: {student.student_id})")
        
        # Check if student has a user account
        if not student.user:
            print("  ❌ No user account found. Creating one...")
            
            # Create user account
            username = student.student_id
            email = f"{student.student_id.lower()}@student.school.com"
            
            # Check if user with this email already exists
            if User.objects.filter(email=email).exists():
                email = f"{student.student_id.lower()}.{student.id}@student.school.com"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=student.first_name,
                last_name=student.last_name
            )
            
            # Set password (use student's existing password or default)
            password = getattr(student, 'password', 'student123')
            user.set_password(password)
            user.save()
            
            # Link user to student
            student.user = user
            student.save()
            
            print(f"  ✅ Created user account with email: {email}")
            print(f"  🔑 Password set to: {password}")
            fixed_count += 1
            
        else:
            print(f"  ✅ User account exists: {student.user.email}")
            
            # Ensure password is set properly
            password = getattr(student, 'password', 'student123')
            if not student.user.has_usable_password():
                student.user.set_password(password)
                student.user.save()
                print(f"  🔑 Password updated to: {password}")
                fixed_count += 1
            else:
                print(f"  🔑 Password is properly set")
    
    print(f"\n✅ Fixed {fixed_count} student accounts")
    
    # Test login for first student
    if students.exists():
        test_student = students.first()
        print(f"\n🧪 Testing login for: {test_student.get_full_name()}")
        print(f"   Student ID: {test_student.student_id}")
        print(f"   Password: {getattr(test_student, 'password', 'student123')}")
        
        # Test authentication
        from django.contrib.auth import authenticate
        user = authenticate(
            username=test_student.user.email, 
            password=getattr(test_student, 'password', 'student123')
        )
        
        if user:
            print("   ✅ Authentication test passed!")
        else:
            print("   ❌ Authentication test failed!")
            
        print(f"\n💡 Try logging in with:")
        print(f"   Student ID: {test_student.student_id}")
        print(f"   Password: {getattr(test_student, 'password', 'student123')}")

if __name__ == "__main__":
    fix_student_login()