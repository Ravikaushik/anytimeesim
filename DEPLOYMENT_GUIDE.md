# AnytimeEsim Deployment Guide

## Overview
This guide will help you deploy your AnytimeEsim Django application to Render with GitHub integration and domain mapping to `anytimeesim.com`.

## Prerequisites
- GitHub account
- Render account
- Domain name (anytimeesim.com) registered with GoDaddy
- Python 3.10+ installed locally

## Step 1: Initialize Git Repository

### Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository named `anytimeesim`
2. Make it public for free Render hosting

### Initialize Local Repository
```bash
# Navigate to your project directory
cd /Users/ravikaushik/Desktop/anytimeesim

# Initialize git repository
git init

# Create .gitignore file
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
*.log
*.pot
*.py[co]
manage.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AnytimeEsim Django application with admin panel, Excel import, and World Pack feature"

# Add remote origin
git remote add origin https://github.com/[YOUR_USERNAME]/anytimeesim.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Prepare for Production

### Create Production Requirements
```bash
# Create production requirements file
cat > requirements.txt << EOF
Django==6.0.2
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-decouple==3.8
Pillow==10.2.0
pandas==2.1.4
openpyxl==3.1.2
EOF
```

### Create Production Settings
```bash
# Create production settings file
cat > anytimesim/settings_production.py << EOF
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['anytimeesim.onrender.com', 'www.anytimeesim.com', 'anytimeesim.com']

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
EOF
```

### Create Procfile for Render
```bash
cat > Procfile << EOF
web: gunicorn anytimesim.wsgi:application
release: python manage.py migrate
EOF
```

### Create Render Build Script
```bash
cat > render-build.sh << EOF
#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

echo "Build completed successfully!"
EOF

chmod +x render-build.sh
```

## Step 3: Deploy to Render

### Create Render Account
1. Go to [Render](https://render.com)
2. Sign up with your GitHub account
3. Connect your GitHub repository

### Create Web Service
1. In Render dashboard, click "New Web Service"
2. Connect your `anytimeesim` repository
3. Configure settings:
   - **Name**: `anytimeesim`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Runtime**: Python 3.11
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `gunicorn anytimesim.wsgi:application`

### Set Environment Variables
In Render dashboard, go to your service settings and add:
- `SECRET_KEY`: Generate a new secret key
- `DEBUG`: `False`
- `DATABASE_URL`: Render will auto-create PostgreSQL database

### Deploy
1. Click "Deploy" button
2. Wait for deployment to complete
3. Render will provide a temporary URL like `https://anytimeesim.onrender.com`

## Step 4: Domain Configuration

### Configure Render Custom Domain
1. In Render dashboard, go to your service
2. Click "Custom Domains"
3. Add `anytimeesim.com`
4. Render will provide DNS records to configure

### Configure GoDaddy DNS
1. Log into your GoDaddy account
2. Go to Domain Manager
3. Select `anytimeesim.com`
4. Click "DNS Management"
5. Add the following records (replace with Render's actual values):

```
Type: A
Host: @
Points to: [Render's IP address]
TTL: 1 Hour

Type: CNAME
Host: www
Points to: [Render's domain]
TTL: 1 Hour
```

### Enable SSL on Render
1. In Render dashboard, go to your service
2. Click "Custom Domains"
3. Click "Verify" next to your domain
4. Render will automatically provision SSL certificate

## Step 5: Final Configuration

### Update Django Settings
```bash
# Update settings to include Render domain
cat >> anytimesim/settings_production.py << EOF

# Update allowed hosts
ALLOWED_HOSTS = [
    'anytimeesim.onrender.com',
    'www.anytimeesim.com', 
    'anytimeesim.com',
    'localhost',
    '127.0.0.1'
]
EOF
```

### Update Database Configuration
```bash
# Install psycopg2 for PostgreSQL
echo "psycopg2-binary==2.9.9" >> requirements.txt
```

### Final Git Push
```bash
git add .
git commit -m "Production deployment: Render configuration and domain setup"
git push origin main
```

## Step 6: Verify Deployment

### Check Website
1. Visit `https://www.anytimeesim.com`
2. Verify all features work:
   - Header visibility
   - Admin panel access
   - Excel import functionality
   - World Pack section
   - Country filtering

### Test Admin Panel
1. Visit `https://www.anytimeesim.com/admin`
2. Create superuser if needed:
   ```bash
   # SSH into Render service or use Render's shell
   python manage.py createsuperuser
   ```

## Troubleshooting

### Common Issues
1. **Static files not loading**: Check `STATIC_ROOT` and `collectstatic`
2. **Database connection**: Verify `DATABASE_URL` environment variable
3. **Domain not resolving**: Check DNS propagation (can take 24-48 hours)
4. **SSL certificate**: Render handles this automatically

### Debug Commands
```bash
# Check logs in Render dashboard
# Or SSH into service and run:
python manage.py check --deploy
python manage.py collectstatic --dry-run --verbosity=3
```

## Maintenance

### Regular Updates
```bash
# Update code
git add .
git commit -m "Feature update"
git push origin main

# Render will auto-deploy
```

### Database Backups
- Render provides automatic daily backups
- Configure backup retention in service settings

### Monitoring
- Use Render's built-in monitoring
- Set up alerts for uptime and performance

## Success! 🎉

Your AnytimeEsim website should now be live at `https://www.anytimeesim.com` with:
- ✅ Professional admin panel
- ✅ Excel import functionality  
- ✅ World Pack feature
- ✅ All 186 countries available
- ✅ Beautiful card designs
- ✅ SSL certificate
- ✅ Custom domain mapping

The deployment is complete and your website is ready for users worldwide!