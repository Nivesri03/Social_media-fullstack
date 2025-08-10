#!/usr/bin/env python3
"""
CAMIGO Social Media Server Startup Script
This script ensures the server starts properly every time.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 50)
    print("    CAMIGO Social Media Server Startup")
    print("=" * 50)
    print()

def check_django():
    """Check if Django is installed and working"""
    try:
        import django
        print(f"✓ Django version: {django.get_version()}")
        return True
    except ImportError:
        print("✗ ERROR: Django not found!")
        print("  Please install requirements: pip install -r requirements.txt")
        return False

def check_database():
    """Check and apply database migrations if needed"""
    print("Checking database migrations...")
    try:
        result = subprocess.run([
            sys.executable, "manage.py", "makemigrations", "--check", "--dry-run"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Applying database migrations...")
            subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
            print("✓ Database migrations applied")
        else:
            print("✓ Database is up to date")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Database error: {e}")
        return False

def collect_static():
    """Collect static files"""
    try:
        subprocess.run([
            sys.executable, "manage.py", "collectstatic", "--noinput"
        ], capture_output=True, check=True)
        print("✓ Static files collected")
        return True
    except subprocess.CalledProcessError:
        print("⚠ Warning: Could not collect static files")
        return True  # Not critical for development

def start_server():
    """Start the Django development server"""
    print()
    print("=" * 50)
    print("    Starting CAMIGO Development Server")
    print("=" * 50)
    print()
    print("Server will be available at:")
    print("  🌐 http://127.0.0.1:8000")
    print("  🌐 http://localhost:8000")
    print()
    print("Login Credentials:")
    print("  👑 Admin: admin / admin123")
    print("  👤 Demo:  demo1 / demo123")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    try:
        # Start server
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ])
        
        # Wait a moment then open browser
        time.sleep(2)
        try:
            webbrowser.open("http://127.0.0.1:8000")
            print("🚀 Browser opened automatically")
        except:
            print("💡 Please open http://127.0.0.1:8000 in your browser")
        
        # Wait for server to finish
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        process.terminate()
    except Exception as e:
        print(f"\n✗ Server error: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check requirements
    if not check_django():
        input("Press Enter to exit...")
        return
    
    if not check_database():
        input("Press Enter to exit...")
        return
    
    collect_static()
    
    # Start server
    start_server()
    
    print("\n👋 Server stopped.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
