# Render Environment Variables Setup

## Backend Environment Variables (school-report-saas.onrender.com)

Set these in your Render backend service dashboard:

```
DEBUG=False
SECRET_KEY=your_actual_django_secret_key_here
ALLOWED_HOSTS=.onrender.com,school-report-saas.onrender.com
CORS_ALLOWED_ORIGINS=https://school-report-saas-1.onrender.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
FRONTEND_URL=https://school-report-saas-1.onrender.com
DATABASE_URL=your_supabase_database_url_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

## Frontend Environment Variables (school-report-saas-1.onrender.com)

Set these in your Render frontend service dashboard:

```
VITE_API_BASE=https://school-report-saas.onrender.com/api
NODE_ENV=production
VITE_APP_ENV=production
VITE_BUILD_SOURCEMAP=false
VITE_BUILD_MINIFY=true
```

## Important Notes

1. Replace `your_actual_django_secret_key_here` with a real Django secret key
2. Replace Supabase URLs and keys with your actual Supabase credentials
3. Replace `your_supabase_database_url_here` with your actual Supabase PostgreSQL connection string