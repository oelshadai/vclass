#!/usr/bin/env python3
"""
Check database schema and fix field name issues
"""
import os
import sys
import django
from django.db import connection

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_report_saas.settings')
django.setup()

def check_database_schema():
    """Check database schema for field name issues"""
    print("Checking database schema...")
    
    with connection.cursor() as cursor:
        # Check terms table
        cursor.execute("PRAGMA table_info(terms)")
        terms_columns = cursor.fetchall()
        print("\nTerms table columns:")
        for col in terms_columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check if there are any uppercase field names
        uppercase_fields = [col for col in terms_columns if col[1] != col[1].lower()]
        if uppercase_fields:
            print(f"\nFound uppercase fields: {[col[1] for col in uppercase_fields]}")
        
        # Check students table
        cursor.execute("PRAGMA table_info(students)")
        students_columns = cursor.fetchall()
        print("\nStudents table columns:")
        for col in students_columns:
            print(f"  {col[1]} ({col[2]})")

def run_migrations():
    """Run Django migrations to ensure schema is up to date"""
    print("\nRunning Django migrations...")
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Migration error: {e}")

if __name__ == "__main__":
    check_database_schema()
    run_migrations()