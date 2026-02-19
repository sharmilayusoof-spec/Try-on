"""
Test image upload functionality
"""
import requests
from PIL import Image
import io

BASE_URL = "http://localhost:8000"


def create_test_image(width=512, height=512, color=(255, 0, 0)):
    """Create a test image"""
    img = Image.new('RGB', (width, height), color)
    
    # Add some pattern
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            img.putpixel((i, j), (255, 255, 255))
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes


def test_upload_endpoints():
    """Test upload endpoints"""
    
    print("🧪 Testing Image Upload Functionality\n")
    
    # Test 1: Upload user image
    print("1. Testing user image upload...")
    try:
        test_img = create_test_image(512, 768, (100, 150, 200))
        files = {'file': ('test_user.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(f"{BASE_URL}/api/v1/upload/user-image", files=files)
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Message: {data['message']}")
            print(f"   URL: {data.get('url', 'N/A')}\n")
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Upload clothing image
    print("2. Testing clothing image upload...")
    try:
        test_img = create_test_image(400, 600, (200, 50, 50))
        files = {'file': ('test_cloth.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(f"{BASE_URL}/api/v1/upload/clothing-image", files=files)
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Message: {data['message']}\n")
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 3: Storage info
    print("3. Testing storage info...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/storage/info")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Directories:")
            for name, info in data.get('directories', {}).items():
                print(f"     - {name}: {info['file_count']} files, {info['total_size_mb']} MB")
            print()
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: List files
    print("4. Testing file listing...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/storage/files")
        
        if response.status_code == 200:
            files = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Total files: {len(files)}")
            if files:
                print(f"   Latest file: {files[0]['filename']} ({files[0]['size_mb']} MB)")
            print()
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 5: Invalid file type
    print("5. Testing invalid file type (should fail)...")
    try:
        files = {'file': ('test.txt', b'not an image', 'text/plain')}
        response = requests.post(f"{BASE_URL}/api/v1/upload/user-image", files=files)
        
        if response.status_code == 400:
            print(f"   ✓ Correctly rejected: {response.status_code}")
            print(f"   Error: {response.json()['detail']}\n")
        else:
            print(f"   ✗ Should have failed but got: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ Upload functionality tests complete!")
    print(f"\n📚 Check uploaded files in: storage/uploads/")


if __name__ == "__main__":
    print("Make sure the server is running: python run.py\n")
    input("Press Enter to start tests...")
    test_upload_endpoints()
