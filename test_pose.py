"""
Test pose detection functionality
"""
import requests
from PIL import Image, ImageDraw
import io

BASE_URL = "http://localhost:8000"


def create_person_silhouette(width=400, height=600):
    """Create a simple person silhouette for testing"""
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Head
    head_center = (width // 2, 80)
    draw.ellipse(
        [head_center[0] - 30, head_center[1] - 30,
         head_center[0] + 30, head_center[1] + 30],
        fill='black'
    )
    
    # Body
    draw.rectangle(
        [width // 2 - 40, 110, width // 2 + 40, 350],
        fill='black'
    )
    
    # Arms
    draw.rectangle([width // 2 - 100, 150, width // 2 - 40, 170], fill='black')
    draw.rectangle([width // 2 + 40, 150, width // 2 + 100, 170], fill='black')
    
    # Legs
    draw.rectangle([width // 2 - 35, 350, width // 2 - 10, 550], fill='black')
    draw.rectangle([width // 2 + 10, 350, width // 2 + 35, 550], fill='black')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG', quality=95)
    img_bytes.seek(0)
    
    return img_bytes


def test_pose_detection():
    """Test pose detection endpoints"""
    
    print("🧪 Testing Pose Detection Module\n")
    
    # Test 1: Get landmark info
    print("1. Testing landmark information...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/pose/landmarks")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Total landmarks: {data['total_landmarks']}")
            print(f"   Model: {data['model_info']['framework']}")
            print(f"   Key groups: {list(data['key_groups'].keys())}\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Detect pose (basic)
    print("2. Testing basic pose detection...")
    try:
        test_img = create_person_silhouette()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/pose/detect",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Detected: {data['detected']}")
            print(f"   Confidence: {data['confidence']:.2f}")
            print(f"   Landmarks: {data['landmark_count']}")
            print(f"   Valid pose: {data['validation']['is_valid']}")
            if data['measurements']:
                print(f"   Measurements: {list(data['measurements'].keys())}")
            print()
        elif response.status_code == 404:
            print(f"   ℹ No pose detected (expected for simple silhouette)")
            print(f"   Try with a real photo for better results\n")
        else:
            print(f"   ✗ Status: {response.status_code}")
            print(f"   Error: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 3: Detect pose (detailed)
    print("3. Testing detailed pose detection...")
    try:
        test_img = create_person_silhouette()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/pose/detect-detailed",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   Detected: {data['detected']}")
            print(f"   Landmarks returned: {len(data.get('landmarks', []))}")
            if data.get('landmarks'):
                sample = data['landmarks'][0]
                print(f"   Sample landmark: {sample['name']}")
                print(f"     Position: ({sample['x']:.3f}, {sample['y']:.3f})")
                print(f"     Visibility: {sample['visibility']:.3f}")
            print()
        elif response.status_code == 404:
            print(f"   ℹ No pose detected (expected for simple silhouette)\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: Visualize pose
    print("4. Testing pose visualization...")
    try:
        test_img = create_person_silhouette()
        files = {'file': ('person.jpg', test_img, 'image/jpeg')}
        
        response = requests.post(
            f"{BASE_URL}/api/v1/pose/visualize",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   File ID: {data['file_id']}")
            print(f"   Message: {data['message']}")
            print(f"   URL: {data.get('url', 'N/A')}")
            print(f"   Check: storage/results/{data['file_id']}.jpg\n")
        elif response.status_code == 404:
            print(f"   ℹ No pose detected for visualization\n")
        else:
            print(f"   ✗ Status: {response.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ Pose detection tests complete!")
    print("\n📝 Note: For best results, use real photos with clear human poses")
    print("   The simple silhouette may not be detected by MediaPipe")
    print("\n💡 Try uploading a real photo through the API docs:")
    print(f"   {BASE_URL}/docs")


if __name__ == "__main__":
    print("Make sure the server is running: python run.py\n")
    input("Press Enter to start tests...")
    test_pose_detection()
