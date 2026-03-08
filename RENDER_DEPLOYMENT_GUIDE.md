# Render Deployment Guide for AnytimeEsim

## Step 1: Create Web Service on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com/
   - Sign up or log in to your account

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository: `Ravikaushik/anytimeesim`

3. **Configure Service Settings**
   ```
   Name: anytimeesim
   Region: Oregon (us-west)
   Branch: main
   Build Command: ./render-build.sh
   Start Command: gunicorn anytimeesim.wsgi:application
   Environment: Python 3.11
   ```

4. **Set Environment Variables**
   Add these environment variables in the Render dashboard:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here (generate a new one)
   ALLOWED_HOSTS=anytimeesim.onrender.com,www.anytimeesim.com,anytimeesim.com
   DATABASE_URL=postgresql://[will be auto-generated]
   ```

5. **Create PostgreSQL Database**
   - Go to "New" → "PostgreSQL"
   - Name: anytimeesim-db
   - Region: Oregon (same as web service)
   - Click "Create Database"
   - Copy the connection string and update DATABASE_URL in environment variables

## Step 2: Configure Domain on GoDaddy

1. **Log into GoDaddy Account**
   - Go to https://dcc.godaddy.com/
   - Select your domain: `anytimeesim.com`

2. **Update DNS Settings**
   - Go to "DNS Management"
   - Add these records:
   
   **A Record:**
   ```
   Type: A
   Host: @
   Points to: [Get IP from Render dashboard]
   TTL: 1 Hour
   ```

   **CNAME Record:**
   ```
   Type: CNAME
   Host: www
   Points to: anytimeesim.onrender.com
   TTL: 1 Hour
   ```

   **TXT Record (for verification):**
   ```
   Type: TXT
   Host: @
   Points to: any verification code from Render
   TTL: 1 Hour
   ```

## Step 3: Configure Domain on Render

1. **Add Custom Domain**
   - Go to your web service on Render
   - Click "Settings" → "Custom Domains"
   - Add: `anytimeesim.com`
   - Add: `www.anytimeesim.com`

2. **Enable SSL Certificate**
   - Render provides free SSL certificates
   - Wait for SSL to be provisioned (usually 5-10 minutes)

## Step 4: Update Django Settings

Update your `anytimeesim/settings.py` for production:

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

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Step 5: Deploy and Test

1. **Trigger Deployment**
   - Push a new commit to trigger deployment
   - Or manually deploy from Render dashboard

2. **Monitor Deployment**
   - Check deployment logs on Render
   - Wait for successful deployment

3. **Test the Website**
   - Visit: https://anytimeesim.onrender.com
   - Test all functionality
   - Check admin panel

## Step 6: Go Live

1. **Update DNS Records**
   - Once deployment is successful, update DNS records on GoDaddy
   - Point to the Render IP address

2. **Wait for DNS Propagation**
   - DNS changes can take 24-48 hours to propagate globally
   - Use https://dnschecker.org/ to check propagation

3. **Verify SSL Certificate**
   - Ensure SSL is working on both domains
   - Check for any SSL warnings

4. **Final Testing**
   - Test the website on www.anytimeesim.com
   - Verify all features work correctly
   - Test admin panel access

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Check STATIC_ROOT and STATICFILES_STORAGE settings
   - Verify collectstatic ran during build

2. **Database Connection Errors**
   - Verify DATABASE_URL format
   - Check database permissions

3. **SSL Certificate Issues**
   - Ensure domain is properly configured on Render
   - Wait for SSL certificate to be provisioned

4. **Migration Errors**
   - Check database permissions
   - Verify migrations are applied

### Getting Help

- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Domain Help: GoDaddy support

## Post-Launch Checklist

- [ ] Website loads on www.anytimeesim.com
- [ ] SSL certificate is active
- [ ] All features work correctly
- [ ] Admin panel is accessible
- [ ] Database is working
- [ ] Static files load properly
- [ ] Email functionality (if needed)
- [ ] Performance monitoring set up
- [ ] Backup strategy configured

## Next Steps

1. **Set up monitoring** (Sentry, New Relic)
2. **Configure backups** for database and media files
3. **Set up analytics** (Google Analytics)
4. **Optimize performance** (CDN, caching)
5. **Security hardening** (firewall, rate limiting)

You're all set! 🚀 Your AnytimeEsim website will be live at www.anytimeesim.com once DNS propagation is complete.