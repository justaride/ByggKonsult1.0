#!/usr/bin/env python3
"""
Oslo Planning Dashboard - Standalone Launcher
Install dependencies and run the application
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required packages for standalone operation"""
    
    required_packages = [
        'streamlit',
        'plotly',
        'pandas', 
        'numpy',
        'sqlite3',  # Usually built-in
        'pdfplumber',
        'openpyxl',  # For Excel support
        'xlsxwriter'
    ]
    
    print("🔧 Installing required packages...")
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
                print(f"✅ {package} (built-in)")
                continue
            
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed")
            
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            print(f"   Try manually: pip install {package}")
        except ImportError:
            # Package not available, try to install
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} installed")
            except:
                print(f"❌ Failed to install {package}")

def check_files():
    """Check if required files exist"""
    required_files = [
        'oslo_standalone_implementation.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def run_application():
    """Run the Streamlit application"""
    print("\n🚀 Starting Oslo Planning Dashboard...")
    print("📱 The application will open in your web browser")
    print("🔄 To stop the application, press Ctrl+C in this terminal")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'oslo_standalone_implementation.py',
            '--server.port=8501',
            '--server.address=localhost'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    print("🏛️ OSLO PLANNING DASHBOARD - STANDALONE")
    print("=" * 50)
    
    # Check if files exist
    if not check_files():
        print("Please ensure oslo_standalone_implementation.py is in the current directory")
        return
    
    # Install dependencies
    install_dependencies()
    
    # Run application
    print("\n" + "=" * 50)
    run_application()

if __name__ == "__main__":
    main()