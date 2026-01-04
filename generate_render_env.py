#!/usr/bin/env python3
"""
Script to generate environment variables for Render deployment
"""

import secrets
import string

def generate_secret_key():
    """Generate a secure Django secret key"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def main():
    print("=== Render Environment Variables Generator ===\n")
    
    # Generate secret key
    secret_key = generate_secret_key()
    
    print("Copy these environment variables to your Render service:\n")
    
    print(f"SECRET_KEY={secret_key}")
    print("DEBUG=False")
    print("ALLOWED_HOSTS=your-app-backend.onrender.com,elitetechreport.netlify.app")
    print()
    
    print("# Database (replace with your Supabase details)")
    print("DATABASE_URL=postgresql://postgres:YOUR_SUPABASE_DB_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres")
    print()
    
    print("# Supabase Configuration")
    print("SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co")
    print("SUPABASE_ANON_KEY=your_anon_key_here")
    print("SUPABASE_SERVICE_KEY=your_service_key_here")
    print("SUPABASE_DB_PASSWORD=your_db_password_here")
    print()
    
    print("# CORS Settings")
    print("CORS_ALLOWED_ORIGINS=https://elitetechreport.netlify.app,http://localhost:5173")
    print("CORS_ALLOW_ALL_ORIGINS=True")
    print("CORS_ALLOW_CREDENTIALS=True")
    print()
    
    print("# Frontend URL")
    print("FRONTEND_URL=https://elitetechreport.netlify.app")
    print()
    
    print("# Email Configuration (optional)")
    print("EMAIL_HOST=smtp.gmail.com")
    print("EMAIL_PORT=587")
    print("EMAIL_HOST_USER=your_email@gmail.com")
    print("EMAIL_HOST_PASSWORD=your_app_password")
    print("EMAIL_USE_TLS=True")
    print("DEFAULT_FROM_EMAIL=your_email@gmail.com")
    print()
    
    print("=== Instructions ===")
    print("1. Replace YOUR_PROJECT_ID with your actual Supabase project ID")
    print("2. Replace placeholder values with your actual Supabase credentials")
    print("3. Update your-app-backend with your actual Render service name")
    print("4. Add these to your Render service environment variables")

if __name__ == "__main__":
    main()