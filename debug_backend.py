"""
Backend Debug Script - Find where execution hangs
"""
import sys
import time
import requests
from io import BytesIO
from PIL import Image
import numpy as np

def create_test_images():
    """Create small test images"""
    print("Creating test images...")
    
    # Create 256x256 test images (small for fast testing)
    person_img = Image.new('RGB', (256, 256), color='blue')
    cloth_img = Image.new('RGB', (256, 256), color='red')
    
    # Save to bytes
    person_bytes = BytesIO()
    cloth_bytes = BytesIO()
    
    person_img.save(person_bytes, format='JPEG')
    cloth_img.save(cloth_bytes, format='JPEG')
    
    person_bytes.seek(0)
    cloth_bytes.seek(0)
    
    print(f"✓ Person image: {person_img.size}")
    print(f"✓ Cloth image: {cloth_img.size}")
    
    return person_bytes, cloth_bytes


def test_backend_with_timeout():
    """Test backend with timeout to detect hanging"""
    print("\n" + "="*60)
    print("BACKEND HANG DETECTION TEST")
    print("="*60)
    
    # Create test images
    person_bytes, cloth_bytes = create_test_images()
    
    # Prepare request
    files = {
        'user_image': ('person.jpg', person_bytes, 'image/jpeg'),
        'cloth_image': ('cloth.jpg', cloth_bytes, 'image/jpeg')
    }
    
    url = 'http://localhost:8000/api/v1/tryon/process'
    
    print(f"\n📤 Sending request to: {url}")
    print("⏱️  Timeout set to 30 seconds")
    print("\nWatching backend console for debug logs...")
    print("If it hangs, check which STEP is the last one printed.\n")
    
    try:
        start = time.time()
        response = requests.post(url, files=files, timeout=30)
        elapsed = time.time() - start
        
        print(f"\n✅ Response received in {elapsed:.2f}s")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Result: {data.get('status')}")
            print(f"Processing time: {data.get('time_taken')}s")
            print(f"Image URL: {data.get('image_url')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        print(f"\n❌ REQUEST TIMEOUT after {elapsed:.2f}s")
        print("\n🔍 DIAGNOSIS:")
        print("   Backend is HANGING during processing")
        print("   Check backend console to see last completed STEP")
        print("\n   Common hang points:")
        print("   - STEP 3: Pose detection (model loading)")
        print("   - STEP 6: TPS warping (nested loops on large images)")
        print("   - STEP 8: Overlay blending (seamless cloning)")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR")
        print("   Backend is not running!")
        print("   Start it with: python run.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   {str(e)}")


def test_tps_performance():
    """Test TPS warping performance with different image sizes"""
    print("\n" + "="*60)
    print("TPS WARPING PERFORMANCE TEST")
    print("="*60)
    
    from app.services.ml.cloth_warping import warp_cloth_to_body
    import cv2
    
    sizes = [(256, 256), (512, 512), (1024, 1024)]
    num_points = 20
    
    for width, height in sizes:
        print(f"\n📏 Testing {width}x{height} image with {num_points} control points...")
        
        # Create test image
        cloth_img = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        # Create random control points
        source_pts = np.random.rand(num_points, 2) * [width, height]
        target_pts = source_pts + np.random.randn(num_points, 2) * 20
        
        try:
            start = time.time()
            warped = warp_cloth_to_body(
                cloth_img,
                source_pts.astype(np.float32),
                target_pts.astype(np.float32),
                (height, width),
                method='tps'
            )
            elapsed = time.time() - start
            
            print(f"   ✓ Completed in {elapsed:.2f}s")
            
            if elapsed > 5:
                print(f"   ⚠️  WARNING: Slow! May cause timeout on real images")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")


def main():
    """Run all diagnostic tests"""
    print("\n" + "="*60)
    print("BACKEND DEBUGGING SUITE")
    print("="*60)
    print("\nThis script will:")
    print("1. Test backend with small images and timeout")
    print("2. Identify which processing step hangs")
    print("3. Test TPS warping performance")
    print("\nMake sure backend is running: python run.py")
    print("\nPress Enter to start...")
    input()
    
    # Test 1: Backend with timeout
    test_backend_with_timeout()
    
    # Test 2: TPS performance (optional)
    print("\n\nRun TPS performance test? (y/n): ", end='')
    if input().lower() == 'y':
        try:
            test_tps_performance()
        except ImportError:
            print("⚠️  Cannot import warping module - skip this test")
    
    print("\n" + "="*60)
    print("DEBUGGING COMPLETE")
    print("="*60)
    print("\n📋 NEXT STEPS:")
    print("1. Check backend console for last completed STEP")
    print("2. If hangs at STEP 6 (warping): Image too large or too many points")
    print("3. If hangs at STEP 8 (overlay): Seamless cloning issue")
    print("4. If hangs at STEP 3 (pose): Model loading issue")
    print("\nSee BACKEND_HANG_FIX.md for solutions\n")


if __name__ == "__main__":
    main()
