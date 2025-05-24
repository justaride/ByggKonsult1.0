#!/usr/bin/env python3
"""
Setup script for Oslo Planning Documents - Premium
Automated setup and verification
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class OsloPlanningSetup:
    """Setup manager for Oslo Planning Premium"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.python_version = sys.version_info
        self.platform_system = platform.system()
        
    def check_system_requirements(self):
        """Check system requirements"""
        print("🔍 Checking system requirements...")
        
        # Check Python version
        if self.python_version < (3, 7):
            print(f"❌ Python 3.7+ required, found {self.python_version.major}.{self.python_version.minor}")
            return False
        else:
            print(f"✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        
        # Check available commands
        commands = ['pip', 'git']
        for cmd in commands:
            if self.check_command(cmd):
                print(f"✅ {cmd} available")
            else:
                print(f"❌ {cmd} not found")
                return False
        
        return True
    
    def check_command(self, command):
        """Check if command is available"""
        try:
            subprocess.run([command, '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        try:
            # Upgrade pip first
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True)
            print("✅ pip upgraded")
            
            # Install requirements
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)], 
                         check=True)
            print("✅ Dependencies installed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def verify_installation(self):
        """Verify installation by testing imports"""
        print("🧪 Verifying installation...")
        
        # Test core imports
        test_imports = [
            ('streamlit', 'Streamlit web framework'),
            ('pandas', 'Data processing'),
            ('plotly', 'Visualizations'),
            ('requests', 'HTTP requests'),
            ('sqlite3', 'Database (built-in)')
        ]
        
        for module, description in test_imports:
            try:
                __import__(module)
                print(f"✅ {description}")
            except ImportError:
                print(f"❌ {description} - import failed")
                return False
        
        # Test main application
        try:
            sys.path.insert(0, str(self.project_root))
            from oslo_planning_premium import OsloPlanningPremium
            
            # Test database creation
            system = OsloPlanningPremium(":memory:")
            docs = system.get_all_documents()
            
            if len(docs) > 0:
                print(f"✅ Application verified - {len(docs)} documents loaded")
                return True
            else:
                print("❌ Application verification failed - no documents")
                return False
                
        except Exception as e:
            print(f"❌ Application verification failed: {e}")
            return False
    
    def create_launch_scripts(self):
        """Create launch scripts for different platforms"""
        print("🚀 Creating launch scripts...")
        
        # Unix/Linux/macOS script
        unix_script = self.project_root / "launch_oslo_premium.sh"
        if unix_script.exists():
            print("✅ Unix launch script exists")
        else:
            print("❌ Unix launch script missing")
        
        # Windows batch script
        windows_script = self.project_root / "launch_oslo_premium.bat"
        if not windows_script.exists():
            windows_content = f"""@echo off
echo 🏛️ Oslo Planning Documents - Premium
echo Starting application...

python oslo_planning_premium.py
if errorlevel 1 (
    echo ❌ Failed to start application
    pause
) else (
    echo ✅ Application started successfully
)
"""
            with open(windows_script, 'w') as f:
                f.write(windows_content)
            print("✅ Windows launch script created")
        
        return True
    
    def setup_development_environment(self):
        """Set up development environment"""
        print("🛠️ Setting up development environment...")
        
        dev_packages = [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=1.0.0'
        ]
        
        try:
            for package in dev_packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True)
            print("✅ Development packages installed")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ Some development packages failed to install")
            return False
    
    def run_tests(self):
        """Run basic tests"""
        print("🧪 Running tests...")
        
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            print("⚠️ Tests directory not found")
            return True
        
        try:
            result = subprocess.run([sys.executable, '-m', 'pytest', str(tests_dir), '-v'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All tests passed")
                return True
            else:
                print("❌ Some tests failed")
                print(result.stdout)
                return False
                
        except FileNotFoundError:
            print("⚠️ pytest not installed, skipping tests")
            return True
    
    def display_summary(self):
        """Display setup summary and next steps"""
        print("\n" + "="*50)
        print("🏆 OSLO PLANNING PREMIUM - SETUP COMPLETE")
        print("="*50)
        print("\n📋 Next Steps:")
        print("1. Launch the application:")
        
        if self.platform_system == "Windows":
            print("   launch_oslo_premium.bat")
        else:
            print("   ./launch_oslo_premium.sh")
        
        print("\n2. Or run directly:")
        print("   streamlit run oslo_planning_premium.py")
        print("\n3. Access the application:")
        print("   http://localhost:8503")
        print("\n📚 Documentation:")
        print("   - README.md - Project overview")
        print("   - docs/DEPLOYMENT.md - Deployment guide")
        print("   - docs/CONTRIBUTING.md - Contribution guide")
        print("\n🎯 Features:")
        print("   - 21 verified Oslo planning documents")
        print("   - Professional UI with enhanced visualizations")
        print("   - Advanced search and analytics")
        print("   - Zero duplicates with quality verification")
        print("\n🆘 Support:")
        print("   - Check docs/ directory for guides")
        print("   - Create GitHub issue for problems")
        print("   - Visit oslo.kommune.no for official information")
        print("\n✅ Setup successful! Ready for production use.")
        print("="*50)
    
    def run_setup(self, include_dev=False, run_tests=False):
        """Run complete setup process"""
        print("🏛️ Oslo Planning Documents - Premium Setup")
        print("=" * 50)
        
        steps = [
            ("System Requirements", self.check_system_requirements),
            ("Dependencies", self.install_dependencies),
            ("Installation Verification", self.verify_installation),
            ("Launch Scripts", self.create_launch_scripts),
        ]
        
        if include_dev:
            steps.append(("Development Environment", self.setup_development_environment))
        
        if run_tests:
            steps.append(("Tests", self.run_tests))
        
        # Execute setup steps
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        # Display summary
        self.display_summary()
        return True


def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Oslo Planning Premium Setup")
    parser.add_argument('--dev', action='store_true', 
                       help='Install development dependencies')
    parser.add_argument('--test', action='store_true', 
                       help='Run tests after setup')
    parser.add_argument('--quick', action='store_true',
                       help='Quick setup (skip optional steps)')
    
    args = parser.parse_args()
    
    setup = OsloPlanningSetup()
    
    if args.quick:
        # Quick setup - just requirements and verification
        success = (setup.check_system_requirements() and 
                  setup.install_dependencies() and 
                  setup.verify_installation())
        if success:
            print("✅ Quick setup complete!")
        else:
            print("❌ Quick setup failed!")
        return success
    else:
        # Full setup
        return setup.run_setup(include_dev=args.dev, run_tests=args.test)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)