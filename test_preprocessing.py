"""
Test preprocessing functionality
"""
import requests
from PIL import Image
import io

BASE_URL = "http://localhost:8000"


def create_test_image(width=800, height=1000, pattern='gradient'):
    """Create a test image with pattern"""
    img = Image.new('RGB', (width, height), 'white')
    pixels = img.load()
    
    if pattern == 'gradient':
        for y in range(height):
            for x in range(width):
                r = int((x / width) * 255)
                g = int((y / height) * 255)
                b = 128
                pixels[x, y] = (r, g, b)
    elif pattern == 'checkerboard':
        square_size = 50
        for y in range(height):
            for x in range(width):
                if ((x // square_size) + (y // square_size)) % 2 == 0:
                    pixels[x, y] = (200, 200, 200)
                else:
                    pixels[x, y] = (50, 50, 50)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes


def test_preprocessing():
    """Test preprocessing endpoints"""
    
    print("🧪 Testing Preprocessing Module\n")
    
    # Test 1: Preprocessing info
    print("1. Testing preprocessing info...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/preprocess/info")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Capabilities: {list(data['capabilities'].keys())}")
            print(f"   Operations: {len(data['supported_operations'])} available")
            print(f"   Batch limit: {data['batch_limit']}\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Preprocess user image
    print("2. Testing user image preprocessing...")
    try:
        test_img = create_test_image(800, 1000, 'gradient')
        files = {'file': ('test_user.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/preprocess/user-image",
            files=files
        )
        
        if response.status_code == 200:
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
    
    # Test 3: Preprocess clothing image
    print("3. Testing clothing image preprocessing...")
    try:
        test_img = create_test_image(600, 600, 'checkerboard')
        files = {'file': ('test_cloth.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/preprocess/clothing-image",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Message: {data['message']}\n")
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: Batch preprocessing
    print("4. Testing batch preprocessing...")
    try:
        files = [
            ('files', ('test1.jpg', create_test_image(400, 400, 'gradient'), 'image/jpeg')),
            ('files', ('test2.jpg', create_test_image(500, 500, 'checkerboard'), 'image/jpeg'))
        ]
        
        response = requests.post(
            f"{BASE_URL}/api/v1/preprocess/batch?image_type=user",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Processed: {len(data)} images")
            for item in data:
                print(f"     - {item['filename']}: {item['message']}")
            print()
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 5: Check processed files
    print("5. Checking processed files...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/storage/info")
        
        if response.status_code == 200:
            data = response.json()
            processed_info = data['directories'].get('processed', {})
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Processed files: {processed_info.get('file_count', 0)}")
            print(f"   Total size: {processed_info.get('total_size_mb', 0)} MB\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ Preprocessing tests complete!")
    print(f"\n📚 Check processed files in: storage/processed/")


if __name__ == "__main__":
    print("Make sure the server is running: python run.py\n")
    input("Press Enter to start tests...")
    test_preprocessing()
