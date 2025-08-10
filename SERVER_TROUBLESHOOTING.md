# CAMIGO Server Troubleshooting Guide

## 🚀 Quick Start (Recommended)

### Option 1: Use the Startup Script
```bash
python start_server.py
```

### Option 2: Use the Batch File (Windows)
```bash
start_server.bat
```

### Option 3: Manual Start
```bash
python manage.py runserver 127.0.0.1:8000
```

## 🔧 Common Issues & Solutions

### Issue 1: "Can't reach this page" / Connection Refused

**Causes:**
- Server not running
- Wrong port/address
- Firewall blocking connection

**Solutions:**
1. Check if server is running in terminal
2. Look for "Starting development server at http://127.0.0.1:8000/"
3. Try different addresses:
   - http://127.0.0.1:8000
   - http://localhost:8000
   - http://0.0.0.0:8000

### Issue 2: Server Won't Start

**Check these:**
```bash
# 1. Check Django installation
python -c "import django; print(django.get_version())"

# 2. Check for errors
python manage.py check

# 3. Apply migrations
python manage.py migrate

# 4. Check port availability
netstat -an | findstr :8000
```

### Issue 3: Database Errors

**Solutions:**
```bash
# Reset database (WARNING: Deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser

# Or just migrate
python manage.py makemigrations
python manage.py migrate
```

### Issue 4: Static Files Not Loading

**Solutions:**
```bash
python manage.py collectstatic --noinput
```

## 🔐 Login Credentials

### Admin Account
- **Username:** admin
- **Password:** admin123
- **Email:** admin@camigo.com

### Demo Accounts
- **Username:** demo1 | **Password:** demo123
- **Username:** demo2 | **Password:** demo123

## 🌐 Server URLs

- **Main Site:** http://127.0.0.1:8000
- **Login Page:** http://127.0.0.1:8000/accounts/login/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 📱 Features Available

- ✅ User Authentication (Login/Register)
- ✅ Instagram-style Homepage
- ✅ Stories Section (centered with posts)
- ✅ Post Creation (Text, Images, Videos)
- ✅ Like/Comment System
- ✅ Split-view Comments (Post left, Comments right)
- ✅ Profile Pages (Instagram-style)
- ✅ Follow/Unfollow System
- ✅ Mobile-responsive Design
- ✅ CAMIGO Branding

## 🆘 Emergency Reset

If nothing works, run this sequence:
```bash
# 1. Stop all servers (Ctrl+C)
# 2. Reset everything
del db.sqlite3
python manage.py migrate
python manage.py shell -c "from accounts.models import User; User.objects.create_superuser('admin', 'admin@camigo.com', 'admin123')"
python manage.py collectstatic --noinput
python manage.py runserver 127.0.0.1:8000
```

## 📞 Need Help?

1. Check terminal output for error messages
2. Ensure Python and Django are properly installed
3. Make sure you're in the correct directory
4. Try restarting your computer if all else fails

## 🎯 Success Indicators

When everything is working, you should see:
- ✅ "Starting development server at http://127.0.0.1:8000/"
- ✅ No error messages in terminal
- ✅ Beautiful CAMIGO login page loads
- ✅ Can login with admin/admin123 or demo1/demo123
