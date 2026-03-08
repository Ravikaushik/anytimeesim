# Railways 500 Error Troubleshooting Guide

## 🔧 **Fix 500 Server Error**

### **Step 1: Update Environment Variables**

Make sure you have these exact environment variables in Railways:

```
SECRET_KEY = xl_b-$ew=5$^ec4jgtdz#r&55at12z9pghst@brm*x6bw%wf)m
DEBUG = False
ALLOWED_HOSTS = anytimeesim-production.up.railway.app,www.anytimeesim.com,anytimeesim.com
DATABASE_URL = sqlite:///db.sqlite3
```

### **Step 2: Check Environment Variable Format**

1. **In Railways Variables section:**
   - Make sure values are **exactly** as shown above
   - No extra quotes around values
   - No extra spaces
   - Use comma to separate multiple hosts in ALLOWED_HOSTS

### **Step 3: Alternative Quick Fix**

If still getting 500 error, try this temporary fix:

```
ALLOWED_HOSTS = *
```

This allows all hosts temporarily.

### **Step 4: Check Railways Logs**

1. **In Railways dashboard:**
   - Go to your project
   - Click on **"Logs"** or **"Deployment Logs"**
   - Look for specific error messages
   - Share the error details if still having issues

### **Step 5: Redeploy**

After updating environment variables:
1. **Click "Deploy" or "Redeploy"**
2. **Wait for deployment to complete**
3. **Try visiting your URL again**

## 🎯 **Common Issues & Solutions**

### **Issue: Environment Variables Not Being Read**
**Solution:** Updated Django settings to properly read from environment variables

### **Issue: Database Connection Error**
**Solution:** Using SQLite database URL format

### **Issue: Static Files Not Found**
**Solution:** Django settings updated for static files

### **Issue: Debug Mode Still On**
**Solution:** DEBUG now reads from environment variable

## 📋 **What Was Fixed**

✅ **SECRET_KEY** - Now reads from environment variable  
✅ **DEBUG** - Now reads from environment variable  
✅ **ALLOWED_HOSTS** - Enhanced parsing from environment variable  
✅ **Django Settings** - Updated for production deployment  

## 🚀 **Next Steps**

1. **Update environment variables** in Railways
2. **Redeploy** your application
3. **Test** your live website
4. **Check logs** if still having issues

## 🆘 **Need More Help?**

If you're still getting a 500 error:
1. **Share your Railways logs**
2. **Confirm environment variables are set correctly**
3. **Try the wildcard ALLOWED_HOSTS fix**

**The Django settings have been updated to properly handle environment variables!** 💪