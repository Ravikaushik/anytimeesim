# AnytimeEsim Deployment Plan

## Overview
Complete deployment plan for deploying AnytimeEsim to Render with domain mapping to anytimeesim.com

## Prerequisites
- [x] Website code completed
- [x] Admin panel functional
- [x] All features working locally
- [ ] GitHub repository setup
- [ ] Render account setup
- [ ] Domain configuration on GoDaddy
- [ ] SSL certificate setup

## Step 1: GitHub Repository Setup

### 1.1 Create .gitignore
```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
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

# Logs
*.log
logs/
```

### 1.2 Create requirements.txt
```txt
Django==6.0.2
Pillow==10.2.0
python-decouple==3.8
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
django-cors-headers==4.3.1
```

### 1.3 Create Procfile
```
web: gunicorn anytimeesim.wsgi:application
release: python manage.py migrate
```

### 1.4 Create render-build.sh
```bash
#!/usr/bin/env bash
# Exit on any error
set -e

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

echo "Build completed successfully!"
```

### 1.5 Commit and Push to GitHub
```bash
git add .
git commit -m "Initial deployment setup with all features"
git push origin main
```

## Step 2: Render Setup

### 2.1 Create Web Service on Render
1. Go to https://dashboard.render.com/
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Configure settings:
   - Name: anytimeesim
   - Region: Oregon (us-west)
   - Branch: main
   - Build Command: `./render-build.sh`
   - Start Command: `gunicorn anytimeesim.wsgi:application`
   - Environment: Python 3.11

### 2.2 Set Environment Variables on Render
```
DEBUG=False
SECRET_KEY=[generate new secret key]
ALLOWED_HOSTS=anytimeesim.onrender.com,www.anytimeesim.com,anytimeesim.com
DATABASE_URL=postgresql://[render database url]
```

### 2.3 Configure Database
1. Create PostgreSQL database on Render
2. Update DATABASE_URL in environment variables
3. Run migrations on deployment

## Step 3: Domain Configuration

### 3.1 Configure DNS on GoDaddy
1. Log into GoDaddy account
2. Go to DNS Management for anytimeesim.com
3. Add these records:
   - A Record: @ → [Render IP address]
   - CNAME: www → anytimeesim.onrender.com
   - TXT Record: _redirect → https://anytimeesim.onrender.com

### 3.2 Configure SSL on Render
1. Go to Render dashboard
2. Select your web service
3. Go to "Settings" → "Custom Domains"
4. Add domain: anytimeesim.com
5. Add domain: www.anytimeesim.com
6. Enable SSL certificate (Render provides free SSL)

## Step 4: Production Settings

### 4.1 Update settings.py
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['anytimeesim.onrender.com', 'www.anytimeesim.com', 'anytimeesim.com']

# Database configuration
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 4.2 Create production environment file
```bash
# .env.production
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=anytimeesim.onrender.com,www.anytimeesim.com,anytimeesim.com
DATABASE_URL=postgresql://username:password@host:port/database
```

## Step 5: Testing and Launch

### 5.1 Pre-launch Checklist
- [ ] All features working on staging
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] SSL certificate active
- [ ] Domain propagation complete
- [ ] Email settings configured (if needed)

### 5.2 Launch Steps
1. Deploy to Render
2. Monitor deployment logs
3. Test all functionality
4. Update DNS records
5. Wait for DNS propagation (24-48 hours)
6. Verify SSL certificate
7. Go live!

## Step 6: Post-Launch

### 6.1 Monitoring
- Set up error tracking (Sentry)
- Monitor performance
- Check logs regularly
- Monitor database usage

### 6.2 Maintenance
- Regular backups
- Security updates
- Performance optimization
- Content updates

## Troubleshooting

### Common Issues
1. **Static files not loading**: Check STATIC_ROOT and STATICFILES_STORAGE
2. **Database connection**: Verify DATABASE_URL format
3. **SSL issues**: Ensure domain is properly configured
4. **Migration errors**: Check database permissions

### Support
- Render documentation: https://render.com/docs
- Django deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Domain help: GoDaddy support