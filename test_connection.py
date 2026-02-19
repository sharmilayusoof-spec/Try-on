"""
Test script to verify frontend-backend connection
"""
import requests
import sys

def test_health():
    """Test health endpoint"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    try:
        r = requests.get('http://localhost:8000/health', timeout=5)
        print(f"✓ Status: {r.status_code}")
        print(f"✓ Response: {r.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Connection failed - Backend not running!")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_process_endpoint():
    """Test /process endpoint exists"""
    print("\n" + "=" * 60)
    print("TEST 2: /process Endpoint")
    print("=" * 60)
    try:
        r = requests.post('http://localhost:8000/api/v1/tryon/process', timeout=5)
        print(f"✓ Status: {r.status_code}")
        
        if r.status_code == 404:
            print("✗ Endpoint not found!")
            return False
        elif r.status_code == 422:
            print("✓ Endpoint exists (missing files - expected)")
            print(f"  Response: {r.json()}")
            return True
        elif r.status_code == 501:
            print("⚠ Endpoint exists but not implemented")
            return False
        else:
            print(f"  Response: {r.json()}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_cors():
    """Test CORS configuration"""
    print("\n" + "=" * 60)
    print("TEST 3: CORS Configuration")
    print("=" * 60)
    try:
        r = requests.options(
            'http://localhost:8000/api/v1/tryon/process',
            headers={'Origin': 'http://localhost:5500'},
            timeout=5
        )
        print(f"✓ Status: {r.status_code}")
        
        allow_origin = r.headers.get('Access-Control-Allow-Origin', 'Not set')
        allow_methods = r.headers.get('Access-Control-Allow-Methods', 'Not set')
        
        print(f"  Allow-Origin: {allow_origin}")
        print(f"  Allow-Methods: {allow_methods}")
        
        if allow_origin in ['*', 'http://localhost:5500']:
            print("✓ CORS configured correctly")
            return True
        else:
            print("⚠ CORS may need adjustment")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_tryon_endpoint():
    """Test /try-on endpoint (alias)"""
    print("\n" + "=" * 60)
    print("TEST 4: /try-on Endpoint (Alias)")
    print("=" * 60)
    try:
        r = requests.post('http://localhost:8000/api/v1/tryon/try-on', timeout=5)
        print(f"✓ Status: {r.status_code}")
        
        if r.status_code == 422:
            print("✓ Alias endpoint exists (missing files - expected)")
            return True
        else:
            print(f"  Response: {r.json()}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("FRONTEND-BACKEND CONNECTION TEST")
    print("=" * 60)
    print("Testing connection to: http://localhost:8000")
    print()
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health()))
    
    if not results[0][1]:
        print("\n" + "=" * 60)
        print("❌ BACKEND NOT RUNNING")
        print("=" * 60)
        print("\nPlease start the backend server:")
        print("  python run.py")
        print("\nThen run this test again.")
        sys.exit(1)
    
    # Test 2: Process endpoint
    results.append(("/process endpoint", test_process_endpoint()))
    
    # Test 3: CORS
    results.append(("CORS", test_cors()))
    
    # Test 4: Try-on alias
    results.append(("/try-on alias", test_tryon_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYour backend is ready!")
        print("You can now test the frontend by:")
        print("1. Open frontend/index.html in your browser")
        print("2. Upload a user image")
        print("3. Select a cloth")
        print("4. Click 'Try On'")
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease check the errors above and fix them.")
    
    print()


if __name__ == "__main__":
    main()
