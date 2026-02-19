"""
Comprehensive Error Checker for Virtual Try-On System
"""
import os
import sys
import requests
from pathlib import Path

def check_backend():
    """Check if backend is running and healthy"""
    print("="*60)
    print("1. BACKEND STATUS CHECK")
    print("="*60)
    
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running")
        print("   Start it with: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False


def check_endpoints():
    """Check if API endpoints exist"""
    print("\n" + "="*60)
    print("2. API ENDPOINTS CHECK")
    print("="*60)
    
    endpoints = [
        ('POST', '/api/v1/tryon/process', 'Main try-on endpoint'),
        ('POST', '/api/v1/tryon/try-on', 'Alias endpoint'),
    ]
    
    all_ok = True
    for method, path, desc in endpoints:
        url = f'http://localhost:8000{path}'
        try:
            response = requests.post(url, timeout=5)
            if response.status_code == 422:
                print(f"✅ {desc}: EXISTS (422 = missing files, expected)")
            elif response.status_code == 404:
                print(f"❌ {desc}: NOT FOUND")
                all_ok = False
            else:
                print(f"✅ {desc}: EXISTS (status {response.status_code})")
        except Exception as e:
            print(f"❌ {desc}: ERROR - {e}")
            all_ok = False
    
    return all_ok


def check_directories():
    """Check if required directories exist"""
    print("\n" + "="*60)
    print("3. DIRECTORY STRUCTURE CHECK")
    print("="*60)
    
    required_dirs = [
        'app',
        'app/api',
        'app/services',
        'app/services/ml',
        'frontend',
        'storage',
        'storage/results',
        'storage/uploads',
        'storage/processed',
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - MISSING")
            all_ok = False
    
    return all_ok


def check_files():
    """Check if critical files exist"""
    print("\n" + "="*60)
    print("4. CRITICAL FILES CHECK")
    print("="*60)
    
    required_files = [
        ('run.py', 'Backend starter'),
        ('app/main.py', 'FastAPI app'),
        ('app/api/v1/endpoints/tryon.py', 'Try-on endpoint'),
        ('app/services/ml/cloth_warping.py', 'Warping module'),
        ('app/services/ml/pose_detection.py', 'Pose detection'),
        ('app/services/ml/overlay_engine.py', 'Overlay engine'),
        ('frontend/index.html', 'Frontend UI'),
        ('frontend/script.js', 'Frontend logic'),
        ('frontend/style.css', 'Frontend styles'),
    ]
    
    all_ok = True
    for file_path, desc in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {desc}: {file_path} ({size} bytes)")
        else:
            print(f"❌ {desc}: {file_path} - MISSING")
            all_ok = False
    
    return all_ok


def check_imports():
    """Check if Python modules can be imported"""
    print("\n" + "="*60)
    print("5. PYTHON IMPORTS CHECK")
    print("="*60)
    
    modules = [
        ('fastapi', 'FastAPI framework'),
        ('uvicorn', 'ASGI server'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('requests', 'Requests'),
    ]
    
    all_ok = True
    for module_name, desc in modules:
        try:
            __import__(module_name)
            print(f"✅ {desc} ({module_name})")
        except ImportError:
            print(f"❌ {desc} ({module_name}) - NOT INSTALLED")
            print(f"   Install with: pip install {module_name}")
            all_ok = False
    
    return all_ok


def check_cors():
    """Check CORS configuration"""
    print("\n" + "="*60)
    print("6. CORS CONFIGURATION CHECK")
    print("="*60)
    
    try:
        response = requests.options(
            'http://localhost:8000/api/v1/tryon/process',
            headers={'Origin': 'http://localhost:5500'},
            timeout=5
        )
        
        allow_origin = response.headers.get('Access-Control-Allow-Origin', 'Not set')
        allow_methods = response.headers.get('Access-Control-Allow-Methods', 'Not set')
        
        print(f"Allow-Origin: {allow_origin}")
        print(f"Allow-Methods: {allow_methods}")
        
        if allow_origin in ['*', 'http://localhost:5500']:
            print("✅ CORS configured correctly")
            return True
        else:
            print("⚠️  CORS may need adjustment for your frontend port")
            return True
    except Exception as e:
        print(f"❌ CORS check failed: {e}")
        return False


def check_recent_errors():
    """Check for common error patterns"""
    print("\n" + "="*60)
    print("7. COMMON ERROR PATTERNS CHECK")
    print("="*60)
    
    # Check if warping is optimized
    warping_file = 'app/services/ml/cloth_warping.py'
    if os.path.exists(warping_file):
        with open(warping_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'points_expanded = points[:, np.newaxis, :]' in content:
                print("✅ TPS warping is OPTIMIZED (vectorized)")
            elif 'for i in range(m):' in content and 'for j in range(n):' in content:
                print("❌ TPS warping uses NESTED LOOPS (will hang!)")
                print("   Apply fix from BACKEND_HANG_FIX.md")
                return False
            else:
                print("⚠️  Cannot verify TPS optimization")
    
    # Check if debug logging is added
    endpoint_file = 'app/api/v1/endpoints/tryon.py'
    if os.path.exists(endpoint_file):
        with open(endpoint_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'STEP 1 COMPLETE' in content:
                print("✅ Debug logging is ENABLED")
            else:
                print("⚠️  Debug logging not found (optional)")
    
    return True


def run_quick_test():
    """Run a quick end-to-end test"""
    print("\n" + "="*60)
    print("8. QUICK END-TO-END TEST")
    print("="*60)
    
    try:
        from io import BytesIO
        from PIL import Image
        
        # Create tiny test images
        person_img = Image.new('RGB', (128, 128), color='blue')
        cloth_img = Image.new('RGB', (128, 128), color='red')
        
        person_bytes = BytesIO()
        cloth_bytes = BytesIO()
        person_img.save(person_bytes, format='JPEG')
        cloth_img.save(cloth_bytes, format='JPEG')
        person_bytes.seek(0)
        cloth_bytes.seek(0)
        
        files = {
            'user_image': ('person.jpg', person_bytes, 'image/jpeg'),
            'cloth_image': ('cloth.jpg', cloth_bytes, 'image/jpeg')
        }
        
        print("Sending test request...")
        response = requests.post(
            'http://localhost:8000/api/v1/tryon/process',
            files=files,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Test PASSED")
            print(f"   Status: {data.get('status')}")
            print(f"   Time: {data.get('time_taken')}s")
            print(f"   Image URL: {data.get('image_url')}")
            return True
        else:
            print(f"❌ Test FAILED: Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Test FAILED: TIMEOUT")
        print("   Backend is hanging during processing")
        print("   Check backend console for last completed STEP")
        return False
    except Exception as e:
        print(f"❌ Test FAILED: {e}")
        return False


def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("VIRTUAL TRY-ON SYSTEM - ERROR CHECKER")
    print("="*60)
    print("\nRunning comprehensive diagnostics...\n")
    
    results = []
    
    # Run all checks
    results.append(("Backend Status", check_backend()))
    
    if not results[0][1]:
        print("\n" + "="*60)
        print("❌ BACKEND NOT RUNNING")
        print("="*60)
        print("\nStart backend first:")
        print("  python run.py")
        print("\nThen run this checker again.")
        return
    
    results.append(("API Endpoints", check_endpoints()))
    results.append(("Directories", check_directories()))
    results.append(("Critical Files", check_files()))
    results.append(("Python Imports", check_imports()))
    results.append(("CORS Config", check_cors()))
    results.append(("Error Patterns", check_recent_errors()))
    results.append(("Quick Test", run_quick_test()))
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED")
        print("="*60)
        print("\nYour system is working correctly!")
        print("\nNext steps:")
        print("1. Open frontend/index.html in browser")
        print("2. Upload user photo and cloth image")
        print("3. Click 'Try On' button")
        print("4. Result should appear within 5 seconds")
    else:
        print("❌ SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease fix the issues above.")
        print("\nCommon solutions:")
        print("- Backend not running: python run.py")
        print("- Missing modules: pip install -r requirements.txt")
        print("- TPS hanging: Apply fix from BACKEND_HANG_FIX.md")
    
    print()


if __name__ == "__main__":
    main()
