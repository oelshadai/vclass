#!/usr/bin/env python3
import os, sys, django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

from students.models import Student
from django.contrib.auth.models import User

student_id = "std_2025BASIC_9004"
password = "8AuoU2"

try:
    student = Student.objects.get(student_id=student_id)
    print(f"Found: {student.get_full_name()}")
    
    if not student.user:
        user = User.objects.create_user(
            username=student_id,
            email=f"{student_id}@school.edu", 
            password=password,
            first_name=student.first_name,
            last_name=student.last_name
        )
        student.user = user
        student.save()
        print("Created User account")
    
    student.password = password
    student.user.set_password(password)
    student.user.is_active = True
    student.user.save()
    student.save()
    print("Fixed password sync")
    
except Exception as e:
    print(f"Error: {e}")