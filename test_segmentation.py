"""
Test segmentation functionality
"""
import requests
from PIL import Image, ImageDraw
import io
import numpy as np

BASE_URL = "http://localhost:8000"


def create_test_person_image(width=400, height=600):
    """Create a simple person image for testing"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw person silhouette
    # Head
    draw.ellipse([width//2-30, 60, width//2+30, 120], fill='black')
    
    # Body
    draw.rectangle([width//2-40, 120, width//2+40, 350], fill='black')
    
    # Arms
    draw.rectangle([width//2-100, 150, width//2-40, 170], fill='black')
    draw.rectangle([width//2+40, 150, width//2+100, 170], fill='black')
    
    # Legs
    draw.rectangle([width//2-35, 350, width//2-10, 550], fill='black')
    draw.rectangle([width//2+10, 350, width//2+35, 550], fill='black')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes


def test_segmentation():
    """Test segmentation endpoints"""
    
    print("🧪 Testing Segmentation Module\n")
    
    # Test 1: Basic segmentation
    print("1. Testing basic segmentation...")
    try:
        test_img = create_test_person_image()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/segmentation/segment",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Method: {data['metadata']['method']}")
            print(f"   Coverage: {data['metadata']['coverage']:.2%}")
            print(f"   Mask URL: {data['mask_url']}\n")
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Segmentation with pose
    print("2. Testing segmentation with pose guidance...")
    try:
        test_img = create_test_person_image()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/segmentation/segment-with-pose",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Pose detected: {data['pose_detected']}")
            print(f"   Coverage: {data['metadata']['coverage']:.2%}\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 3: Extract person
    print("3. Testing person extraction...")
    try:
        test_img = create_test_person_image()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/segmentation/extract-person",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Message: {data['message']}")
            print(f"   URL: {data['url']}\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: Detect regions
    print("4. Testing region detection...")
    try:
        test_img = create_test_person_image()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/segmentation/detect-regions",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Regions: {', '.join(data['regions'])}")
            print(f"   Message: {data['message']}\n")
        elif response.status_code == 404:
            print(f"   ℹ No pose detected (expected for simple silhouette)\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 5: Cloth region detection
    print("5. Testing cloth region detection...")
    try:
        test_img = create_test_person_image()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        for cloth_type in ['shirt', 'pants']:
            response = requests.post(
                f"{BASE_URL}/api/v1/segmentation/cloth-region?cloth_type={cloth_type}",
                files=files
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ {cloth_type.capitalize()}: Coverage {data['coverage']:.2%}")
            elif response.status_code == 404:
                print(f"   ℹ {cloth_type.capitalize()}: No pose detected")
        print()
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ Segmentation tests complete!")
    print("\n📝 Note: For best results, use real photos with clear person")
    print("   The simple silhouette may not segment perfectly")
    print("\n💡 Check results in:")
    print("   - storage/processed/ (masks)")
    print("   - storage/results/ (extracted images)")


if __name__ == "__main__":
    print("Make sure the server is running: python run.py\n")
    input("Press Enter to start tests...")
    test_segmentation()
