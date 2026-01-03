#!/usr/bin/env python
"""
Debug script to check student assignments
Run this from the backend directory: python debug_student_assignments.py
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

from assignments.models import Assignment, StudentAssignment
from students.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_assignments():
    print("=== ASSIGNMENT DEBUG ===")
    
    # Get all assignments
    assignments = Assignment.objects.all()
    print(f"\nTotal Assignments: {assignments.count()}")
    
    for assignment in assignments:
        print(f"\nAssignment: {assignment.title}")
        print(f"  Status: {assignment.status}")
        print(f"  Class: {assignment.class_instance}")
        print(f"  Created by: {assignment.created_by.email if assignment.created_by else 'Unknown'}")
        
        # Get students in this class
        students_in_class = Student.objects.filter(
            current_class=assignment.class_instance,
            is_active=True
        )
        print(f"  Students in class: {students_in_class.count()}")
        
        # Get student assignments for this assignment
        student_assignments = StudentAssignment.objects.filter(assignment=assignment)
        print(f"  Student assignments created: {student_assignments.count()}")
        
        if student_assignments.count() < students_in_class.count():
            print(f"  ⚠️  MISSING STUDENT ASSIGNMENTS!")
            missing_students = students_in_class.exclude(
                id__in=student_assignments.values_list('student_id', flat=True)
            )
            print(f"  Missing for students: {[s.get_full_name() for s in missing_students]}")
    
    print("\n=== STUDENT ASSIGNMENTS ===")
    
    # Get all students
    students = Student.objects.filter(is_active=True)
    print(f"\nTotal Active Students: {students.count()}")
    
    for student in students:
        print(f"\nStudent: {student.get_full_name()}")
        print(f"  Class: {student.current_class}")
        print(f"  User account: {'Yes' if student.user else 'No'}")
        
        # Get assignments for this student
        student_assignments = StudentAssignment.objects.filter(student=student)
        print(f"  Total assignments: {student_assignments.count()}")
        
        # Get published assignments for student's class
        if student.current_class:
            published_assignments = Assignment.objects.filter(
                class_instance=student.current_class,
                status='PUBLISHED'
            )
            print(f"  Published assignments in class: {published_assignments.count()}")
            
            if student_assignments.count() < published_assignments.count():
                print(f"  ⚠️  MISSING ASSIGNMENTS!")

def fix_missing_assignments():
    print("\n=== FIXING MISSING ASSIGNMENTS ===")
    
    # Get all published assignments
    published_assignments = Assignment.objects.filter(status='PUBLISHED')
    
    for assignment in published_assignments:
        print(f"\nFixing assignment: {assignment.title}")
        
        # Get students in this class
        students = Student.objects.filter(
            current_class=assignment.class_instance,
            is_active=True
        )
        
        created_count = 0
        for student in students:
            student_assignment, created = StudentAssignment.objects.get_or_create(
                assignment=assignment,
                student=student,
                defaults={'status': 'NOT_STARTED'}
            )
            if created:
                created_count += 1
                print(f"  ✓ Created assignment for: {student.get_full_name()}")
        
        if created_count > 0:
            print(f"  Created {created_count} new student assignments")
        else:
            print(f"  No missing assignments found")

if __name__ == "__main__":
    debug_assignments()
    
    # Ask if user wants to fix missing assignments
    fix = input("\nDo you want to fix missing assignments? (y/n): ")
    if fix.lower() == 'y':
        fix_missing_assignments()
        print("\n=== VERIFICATION ===")
        debug_assignments()