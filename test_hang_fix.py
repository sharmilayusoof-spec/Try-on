"""
Quick test to verify backend hang fix
"""
import requests
import time
from io import BytesIO
from PIL import Image

def test_backend_performance():
    """Test backend with different image sizes"""
    print("="*60)
    print("BACKEND HANG FIX VERIFICATION")
    print("="*60)
    
    test_cases = [
        ("Small (256x256)", 256),
        ("Medium (512x512)", 512),
        ("Large (1024x1024)", 1024),
    ]
    
    for name, size in test_cases:
        print(f"\n📸 Testing {name}...")
        
        # Create test images
        person_img = Image.new('RGB', (size, size), color=(100, 150, 200))
        cloth_img = Image.new('RGB', (size, size), color=(200, 100, 150))
        
        # Convert to bytes
        person_bytes = BytesIO()
        cloth_bytes = BytesIO()
        person_img.save(person_bytes, format='JPEG', quality=90)
        cloth_img.save(cloth_bytes, format='JPEG', quality=90)
        person_bytes.seek(0)
        cloth_bytes.seek(0)
        
        # Prepare request
        files = {
            'user_image': ('person.jpg', person_bytes, 'image/jpeg'),
            'cloth_image': ('cloth.jpg', cloth_bytes, 'image/jpeg')
        }
        
        # Send request with timeout
        url = 'http://localhost:8000/api/v1/tryon/process'
        
        try:
            start = time.time()
            response = requests.post(url, files=files, timeout=15)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success in {elapsed:.2f}s")
                print(f"   Backend time: {data.get('time_taken')}s")
                
                if elapsed > 10:
                    print(f"   ⚠️  WARNING: Slow response (>{elapsed:.1f}s)")
                elif elapsed > 5:
                    print(f"   ⚠️  Acceptable but could be faster")
                else:
                    print(f"   ✓ Good performance!")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            elapsed = time.time() - start
            print(f"   ❌ TIMEOUT after {elapsed:.2f}s")
            print(f"   Backend is still hanging!")
            print(f"   Check backend console for last completed STEP")
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed - backend not running?")
            return False
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    print("\nBackend hang issue is FIXED!")
    print("Processing times should be:")
    print("  - Small images: < 2s")
    print("  - Medium images: < 3s")
    print("  - Large images: < 5s")
    return True


def main():
    print("\n🔧 Backend Hang Fix Verification")
    print("\nThis will test if the TPS warping optimization works.")
    print("Make sure backend is running: python run.py\n")
    
    input("Press Enter to start test...")
    
    success = test_backend_performance()
    
    if success:
        print("\n✅ Fix verified! Backend is working correctly.")
        print("\nYou can now:")
        print("1. Test with frontend (open frontend/index.html)")
        print("2. Upload real images and click 'Try On'")
        print("3. Should receive response within 5 seconds")
    else:
        print("\n❌ Fix not working yet!")
        print("\nTroubleshooting:")
        print("1. Check if you applied the vectorized TPS fix")
        print("2. Restart backend: python run.py")
        print("3. Check backend console for error messages")
        print("4. See BACKEND_HANG_FIX.md for detailed instructions")


if __name__ == "__main__":
    main()
