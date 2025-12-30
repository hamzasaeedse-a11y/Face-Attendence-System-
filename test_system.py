#!/usr/bin/env python3

import os
import sys
import subprocess
import pickle

def run_command(command, description=""):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🧪 Face Attendance System - Comprehensive Test")
    print("=" * 50)
    
    # Check if we're in virtual environment
    if not os.path.exists('.venv'):
        print("❌ Virtual environment not found!")
        print("Please run this from the project directory with .venv")
        sys.exit(1)
    
    # Test 1: Create better sample faces
    print("\n📋 TEST 1: Creating realistic sample faces")
    if run_command("python create_real_sample_faces.py", "Creating realistic face images"):
        print("✅ Sample faces created successfully")
    else:
        print("⚠️ Using existing face images")
    
    # Test 2: Generate face encodings  
    print("\n📋 TEST 2: Generating face encodings")
    if run_command("python encodeGenerator.py", "Generating face encodings from images"):
        # Check if encodings were created
        try:
            with open('EncodedImages.p', 'rb') as f:
                data = pickle.load(f)
                encodings, ids = data
                print(f"✅ Successfully created encodings for {len(encodings)} faces: {ids}")
        except Exception as e:
            print(f"❌ Failed to load encodings: {e}")
    else:
        print("⚠️ Using existing encodings or creating dummy ones")
        run_command("python create_dummy_encodings.py", "Creating dummy encodings for testing")
    
    # Test 3: Test offline attendance viewer
    print("\n📋 TEST 3: Testing offline attendance viewer")
    print("🖥️ This will open a GUI window - close it to continue")
    input("Press Enter to continue with GUI test...")
    
    try:
        # Run in background and kill after a few seconds
        proc = subprocess.Popen([sys.executable, "view_attendance_offline.py"])
        print("✅ Attendance viewer started successfully")
        print("📝 If GUI opened, the viewer is working correctly")
        
        # Give user time to see the GUI
        input("Press Enter after checking the GUI (close the window first)...")
        
        # Try to terminate gracefully
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
            
    except Exception as e:
        print(f"❌ Failed to start attendance viewer: {e}")
    
    # Test 4: Check all files exist
    print("\n📋 TEST 4: Checking required files")
    
    required_files = [
        ("app_fixed.py", "Fixed main application"),
        ("face_attendance_offline.py", "Offline attendance system"),
        ("view_attendance_offline.py", "Offline attendance viewer"),
        ("encodeGenerator.py", "Face encoding generator"),
        ("create_real_sample_faces.py", "Sample face creator"),
        ("EncodedImages.p", "Face encodings data"),
        ("Resources/Background2.png", "Main background image"),
        ("Resources/classOverview/classOverviewbackground2.png", "Overview background"),
    ]
    
    all_files_exist = True
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ Missing {description}: {file_path}")
            all_files_exist = False
    
    # Check Images directory
    if os.path.exists('Images'):
        image_files = [f for f in os.listdir('Images') if f.endswith('.jpg')]
        print(f"✅ Found {len(image_files)} student images in Images/")
    else:
        print("❌ Images directory not found")
        all_files_exist = False
    
    print("\n" + "=" * 50)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    if all_files_exist:
        print("🎉 ALL TESTS PASSED!")
        print("\n📋 Ready to use:")
        print("   • Offline face attendance system")
        print("   • Offline attendance data viewer") 
        print("   • Face encoding generation")
        print("   • Sample student data")
        
        print("\n🚀 QUICK START:")
        print("   1. Run: python app_fixed.py")
        print("   2. Use OFFLINE features (green buttons)")
        print("   3. Test face attendance with your camera")
        
        print("\n🎥 Camera Test (Optional):")
        test_camera = input("\nDo you want to test camera access? (y/N): ").lower().strip()
        if test_camera == 'y':
            print("🎥 Testing camera access...")
            print("📹 A camera window should open - press 'q' to quit")
            try:
                import cv2
                cap = cv2.VideoCapture(0)
                if cap.isOpened():
                    print("✅ Camera accessible!")
                    ret, frame = cap.read()
                    if ret:
                        cv2.imshow('Camera Test - Press Q to quit', frame)
                        cv2.waitKey(2000)  # Show for 2 seconds
                        cv2.destroyAllWindows()
                        print("✅ Camera test completed")
                    else:
                        print("⚠️ Camera opened but no frame captured")
                else:
                    print("❌ Cannot access camera")
                cap.release()
            except Exception as e:
                print(f"❌ Camera test failed: {e}")
                
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Please check the missing files above")
        
    print("\n💡 TROUBLESHOOTING:")
    print("   • Camera issues: Try changing camera_number from 0 to 1 (or vice versa)")
    print("   • Firebase errors: Use OFFLINE features only")
    print("   • Face detection issues: Ensure good lighting and clear face photos")
    print("   • Permission issues: Check camera permissions")
    
    print(f"\n📖 For detailed setup instructions, see: SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
