# Render + Supabase Deployment Guide

## Prerequisites
1. Supabase project created at https://supabase.com
2. Render account at https://render.com
3. GitHub repository with your code

## Step 1: Get Supabase Credentials

From your Supabase dashboard:
1. Go to Settings > API
2. Copy these values:
   - Project URL (SUPABASE_URL)
   - Anon public key (SUPABASE_ANON_KEY)
   - Service role key (SUPABASE_SERVICE_KEY)
3. Go to Settings > Database
4. Copy the database password (SUPABASE_DB_PASSWORD)

## Step 2: Deploy Backend to Render

1. Go to Render dashboard
2. Click "New" > "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: your-app-backend
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn school_report_saas.wsgi:application`
   - Instance Type: Free (or paid for better performance)

5. Add Environment Variables:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-backend.onrender.com,elitetechreport.netlify.app
   DATABASE_URL=postgresql://postgres:YOUR_SUPABASE_DB_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
   
   SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_key
   SUPABASE_DB_PASSWORD=your_db_password
   
   CORS_ALLOWED_ORIGINS=https://elitetechreport.netlify.app,http://localhost:5173
   CORS_ALLOW_ALL_ORIGINS=True
   CORS_ALLOW_CREDENTIALS=True
   
   FRONTEND_URL=https://elitetechreport.netlify.app
   
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   ```

6. Deploy the service

## Step 3: Update Frontend Configuration

Update your frontend `.env.production`:
```
VITE_API_BASE=https://your-app-backend.onrender.com/api
VITE_SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
```

## Step 4: Run Database Migrations

After backend deployment:
1. Go to Render dashboard > your service
2. Open Shell tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Step 5: Test the Connection

1. Check backend health: `https://your-app-backend.onrender.com/api/`
2. Test frontend connection to backend
3. Verify database operations work

## Troubleshooting

### Common Issues:
1. **Database connection fails**: Check DATABASE_URL format and credentials
2. **CORS errors**: Verify CORS_ALLOWED_ORIGINS includes your frontend URL
3. **Static files not loading**: Ensure WhiteNoise is configured
4. **Migrations fail**: Check database permissions and connection

### Debug Commands:
```bash
# Check database connection
python manage.py dbshell

# View logs
python manage.py check --deploy

# Test migrations
python manage.py showmigrations
```

## Security Notes
- Never commit real credentials to Git
- Use strong SECRET_KEY in production
- Enable SSL/HTTPS for all connections
- Regularly rotate API keys