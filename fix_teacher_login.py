#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.contrib.auth import get_user_model
from teachers.models import Teacher

User = get_user_model()

def fix_teacher_login():
    """Diagnose and fix teacher login issues"""
    
    print("🔍 Checking teacher accounts...")
    
    # List all teachers
    teachers = Teacher.objects.all()
    if not teachers.exists():
        print("❌ No teachers found in the system")
        return
    
    print(f"📋 Found {teachers.count()} teacher(s):")
    
    for i, teacher in enumerate(teachers, 1):
        user = teacher.user
        print(f"\n{i}. Teacher: {teacher.get_full_name()}")
        print(f"   Email: {user.email}")
        print(f"   Employee ID: {teacher.employee_id}")
        print(f"   Role: {user.role}")
        print(f"   Active: {user.is_active}")
        print(f"   School: {user.school.name if user.school else 'No school'}")
    
    # Ask which teacher to fix
    try:
        choice = input(f"\nEnter teacher number to fix (1-{teachers.count()}): ")
        teacher_index = int(choice) - 1
        
        if teacher_index < 0 or teacher_index >= teachers.count():
            print("❌ Invalid choice")
            return
            
        selected_teacher = list(teachers)[teacher_index]
        user = selected_teacher.user
        
        print(f"\n🔧 Fixing login for: {selected_teacher.get_full_name()}")
        print(f"   Email: {user.email}")
        
        # Reset password
        new_password = input("Enter new password (or press Enter for 'teacher123'): ").strip()
        if not new_password:
            new_password = "teacher123"
        
        user.set_password(new_password)
        user.is_active = True
        user.save()
        
        print(f"\n✅ Login credentials updated!")
        print(f"📧 Email/Username: {user.email}")
        print(f"🔑 Password: {new_password}")
        print(f"🌐 Login URL: http://localhost:3000/login")
        print(f"\nℹ️  Use the EMAIL as username, not employee ID")
        
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Operation cancelled")
        return

if __name__ == '__main__':
    fix_teacher_login()