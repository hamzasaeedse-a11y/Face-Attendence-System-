#!/usr/bin/env python3

import os
import sys
import subprocess
import pickle

def check_requirement(name, check_func, fix_msg=""):
    """Check a requirement and report status"""
    try:
        result = check_func()
        if result:
            print(f"✅ {name}: OK")
            return True
        else:
            print(f"❌ {name}: FAILED")
            if fix_msg:
                print(f"   Fix: {fix_msg}")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        if fix_msg:
            print(f"   Fix: {fix_msg}")
        return False

def main():
    print("🔍 Face Attendance System - Installation Verification")
    print("=" * 55)
    
    all_checks_passed = True
    
    # Check Python version
    def check_python():
        return sys.version_info >= (3, 8)
    
    if not check_requirement("Python 3.8+", check_python):
        all_checks_passed = False
    
    # Check virtual environment
    def check_venv():
        return os.path.exists('.venv') and os.path.exists('.venv/bin/activate')
    
    if not check_requirement("Virtual Environment", check_venv, "Run: python -m venv .venv"):
        all_checks_passed = False
    
    # Check core dependencies
    core_packages = [
        'opencv-python',
        'face-recognition', 
        'numpy',
        'firebase-admin',
        'pandas',
        'openpyxl',
        'Pillow'
    ]
    
    def check_package(pkg_name):
        def check():
            result = subprocess.run(['.venv/bin/pip', 'show', pkg_name], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        return check
    
    for pkg in core_packages:
        if not check_requirement(f"Package: {pkg}", check_package(pkg), 
                                f"Run: source .venv/bin/activate && pip install {pkg}"):
            all_checks_passed = False
    
    # Check tkinter (system package)
    def check_tkinter():
        try:
            import tkinter
            return True
        except ImportError:
            return False
    
    if not check_requirement("Tkinter (GUI support)", check_tkinter, 
                            "Run: sudo apt install python3-tk"):
        all_checks_passed = False
    
    # Check directory structure
    required_dirs = [
        ('Resources', 'UI resources directory'),
        ('Resources/StudentDetailsArea', 'Student details UI'),  
        ('Resources/classOverview', 'Class overview UI'),
        ('Images', 'Student photos directory')
    ]
    
    for dir_path, description in required_dirs:
        def check_dir(path=dir_path):
            return os.path.exists(path) and os.path.isdir(path)
        
        if not check_requirement(f"Directory: {description}", check_dir, 
                                f"Create: mkdir -p {dir_path}"):
            all_checks_passed = False
    
    # Check required files
    required_files = [
        ('app.py', 'Main GUI application'),
        ('face_attendance.py', 'Face recognition system'),
        ('encodeGenerator.py', 'Face encoding generator'),
        ('requirements.txt', 'Dependencies list'),
        ('EncodedImages.p', 'Face encodings data'),
        ('Resources/Background2.png', 'Main background'),
        ('Resources/classOverview/classOverviewbackground2.png', 'Class overview background')
    ]
    
    for file_path, description in required_files:
        def check_file(path=file_path):
            return os.path.exists(path) and os.path.isfile(path)
        
        if not check_requirement(f"File: {description}", check_file):
            all_checks_passed = False
    
    # Check face encodings
    def check_encodings():
        try:
            with open('EncodedImages.p', 'rb') as f:
                data = pickle.load(f)
                encodings, ids = data
                return len(encodings) > 0 and len(ids) > 0
        except:
            return False
    
    if not check_requirement("Face Encodings", check_encodings, 
                           "Run: source .venv/bin/activate && python encodeGenerator.py"):
        all_checks_passed = False
    
    # Check sample images
    def check_sample_images():
        image_files = [f for f in os.listdir('Images') if f.endswith('.jpg')]
        return len(image_files) > 0
    
    if not check_requirement("Sample Images", check_sample_images,
                           "Run: source .venv/bin/activate && python create_sample_students.py"):
        all_checks_passed = False
    
    print("\n" + "=" * 55)
    
    if all_checks_passed:
        print("🎉 INSTALLATION COMPLETE! All checks passed.")
        print("\n📋 Quick Start:")
        print("   1. Activate virtual environment: source .venv/bin/activate")
        print("   2. Run main application: python app.py")
        print("   3. For Firebase features, update the credentials file")
        print("\n📖 For detailed instructions, see SETUP_GUIDE.md")
    else:
        print("❌ INSTALLATION INCOMPLETE! Some checks failed.")
        print("   Please fix the issues above and run this verification again.")
    
    print("\n🔧 Component Test Commands:")
    print("   • Test GUI: python app.py")
    print("   • Generate encodings: python encodeGenerator.py") 
    print("   • Create sample data: python create_sample_students.py")
    print("   • View this help: python verify_installation.py")

if __name__ == "__main__":
    main()
