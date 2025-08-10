@echo off
echo ========================================
echo    CAMIGO Social Media Server Startup
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Django installation...
python -c "import django; print(f'Django version: {django.get_version()}')" 2>nul
if errorlevel 1 (
    echo ERROR: Django not found! Please install requirements.
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Checking for database migrations...
python manage.py makemigrations --check --dry-run >nul 2>&1
if errorlevel 1 (
    echo Applying database migrations...
    python manage.py migrate
)

echo.
echo Collecting static files...
python manage.py collectstatic --noinput >nul 2>&1

echo.
echo ========================================
echo    Starting CAMIGO Development Server
echo ========================================
echo.
echo Server will be available at:
echo   http://127.0.0.1:8000
echo   http://localhost:8000
echo.
echo Login Credentials:
echo   Admin: admin / admin123
echo   Demo:  demo1 / demo123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 127.0.0.1:8000

echo.
echo Server stopped.
pause
