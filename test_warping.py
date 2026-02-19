"""
Test script for cloth warping endpoints
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"


def test_warping_info():
    """Test warping info endpoint"""
    print("\n=== Testing Warping Info ===")
    
    response = requests.get(f"{BASE_URL}/warping/warping-info")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Warping info retrieved")
        print(f"Available methods: {list(data['methods'].keys())}")
        print(f"Cloth types: {list(data['cloth_types'].keys())}")
        print(f"Performance estimate: {data['performance']['total_estimate']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_warp_cloth(person_path: str, cloth_path: str, cloth_type: str = 'shirt'):
    """Test general cloth warping"""
    print(f"\n=== Testing Cloth Warping ({cloth_type}) ===")
    
    if not os.path.exists(person_path):
        print(f"❌ Person image not found: {person_path}")
        return
    
    if not os.path.exists(cloth_path):
        print(f"❌ Cloth image not found: {cloth_path}")
        return
    
    with open(person_path, 'rb') as pf, open(cloth_path, 'rb') as cf:
        files = {
            'person_image': ('person.jpg', pf, 'image/jpeg'),
            'cloth_image': ('cloth.jpg', cf, 'image/jpeg')
        }
        
        params = {
            'cloth_type': cloth_type,
            'method': 'tps',
            'apply_perspective': True,
            'apply_curvature': True
        }
        
        response = requests.post(
            f"{BASE_URL}/warping/warp-cloth",
            files=files,
            params=params
        )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {cloth_type.capitalize()} warped successfully")
        print(f"File ID: {data['file_id']}")
        print(f"Method: {data['warping_method']}")
        print(f"Scale factor: {data['scale_factor']:.2f}")
        print(f"Control points: {data['control_points']['source']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_warp_shirt(person_path: str, shirt_path: str):
    """Test shirt-specific warping"""
    print("\n=== Testing Shirt Warping ===")
    
    if not os.path.exists(person_path):
        print(f"❌ Person image not found: {person_path}")
        return
    
    if not os.path.exists(shirt_path):
        print(f"❌ Shirt image not found: {shirt_path}")
        return
    
    with open(person_path, 'rb') as pf, open(shirt_path, 'rb') as sf:
        files = {
            'person_image': ('person.jpg', pf, 'image/jpeg'),
            'shirt_image': ('shirt.jpg', sf, 'image/jpeg')
        }
        
        response = requests.post(
            f"{BASE_URL}/warping/warp-shirt",
            files=files,
            params={'method': 'tps'}
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Shirt warped successfully")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_warp_pants(person_path: str, pants_path: str):
    """Test pants-specific warping"""
    print("\n=== Testing Pants Warping ===")
    
    if not os.path.exists(person_path):
        print(f"❌ Person image not found: {person_path}")
        return
    
    if not os.path.exists(pants_path):
        print(f"❌ Pants image not found: {pants_path}")
        return
    
    with open(person_path, 'rb') as pf, open(pants_path, 'rb') as pf2:
        files = {
            'person_image': ('person.jpg', pf, 'image/jpeg'),
            'pants_image': ('pants.jpg', pf2, 'image/jpeg')
        }
        
        response = requests.post(
            f"{BASE_URL}/warping/warp-pants",
            files=files,
            params={'method': 'tps'}
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Pants warped successfully")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_warping_methods(person_path: str, cloth_path: str):
    """Test different warping methods"""
    print("\n=== Testing Warping Methods ===")
    
    methods = ['tps', 'affine']
    
    for method in methods:
        print(f"\nTesting {method.upper()} method...")
        
        if not os.path.exists(person_path) or not os.path.exists(cloth_path):
            print("❌ Images not found")
            continue
        
        with open(person_path, 'rb') as pf, open(cloth_path, 'rb') as cf:
            files = {
                'person_image': ('person.jpg', pf, 'image/jpeg'),
                'cloth_image': ('cloth.jpg', cf, 'image/jpeg')
            }
            
            response = requests.post(
                f"{BASE_URL}/warping/warp-cloth",
                files=files,
                params={
                    'cloth_type': 'shirt',
                    'method': method,
                    'apply_perspective': True,
                    'apply_curvature': True
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {method.upper()} warping successful")
            print(f"   File ID: {data['file_id']}")
        else:
            print(f"❌ {method.upper()} failed: {response.status_code}")


def test_transformation_options(person_path: str, cloth_path: str):
    """Test different transformation options"""
    print("\n=== Testing Transformation Options ===")
    
    options = [
        {'perspective': True, 'curvature': True, 'name': 'Full'},
        {'perspective': True, 'curvature': False, 'name': 'Perspective only'},
        {'perspective': False, 'curvature': True, 'name': 'Curvature only'},
        {'perspective': False, 'curvature': False, 'name': 'None'}
    ]
    
    for opt in options:
        print(f"\nTesting {opt['name']}...")
        
        if not os.path.exists(person_path) or not os.path.exists(cloth_path):
            print("❌ Images not found")
            continue
        
        with open(person_path, 'rb') as pf, open(cloth_path, 'rb') as cf:
            files = {
                'person_image': ('person.jpg', pf, 'image/jpeg'),
                'cloth_image': ('cloth.jpg', cf, 'image/jpeg')
            }
            
            response = requests.post(
                f"{BASE_URL}/warping/warp-cloth",
                files=files,
                params={
                    'cloth_type': 'shirt',
                    'method': 'tps',
                    'apply_perspective': opt['perspective'],
                    'apply_curvature': opt['curvature']
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {opt['name']} successful")
            print(f"   Transformations: {data['transformations_applied']}")
        else:
            print(f"❌ Failed: {response.status_code}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("CLOTH WARPING MODULE TEST SUITE")
    print("=" * 60)
    
    # Test info endpoint (no images needed)
    test_warping_info()
    
    # Define test image paths
    # You can modify these paths to point to your test images
    person_image = "test_person.jpg"
    shirt_image = "test_shirt.jpg"
    pants_image = "test_pants.jpg"
    
    # Check if test images exist
    print("\n=== Checking Test Images ===")
    if os.path.exists(person_image):
        print(f"✅ Person image found: {person_image}")
    else:
        print(f"⚠️  Person image not found: {person_image}")
        print("   Please provide a test image with a person")
    
    if os.path.exists(shirt_image):
        print(f"✅ Shirt image found: {shirt_image}")
    else:
        print(f"⚠️  Shirt image not found: {shirt_image}")
        print("   Please provide a test shirt image")
    
    if os.path.exists(pants_image):
        print(f"✅ Pants image found: {pants_image}")
    else:
        print(f"⚠️  Pants image not found: {pants_image}")
        print("   Please provide a test pants image")
    
    # Run tests if images exist
    if os.path.exists(person_image) and os.path.exists(shirt_image):
        test_warp_cloth(person_image, shirt_image, 'shirt')
        test_warp_shirt(person_image, shirt_image)
        test_warping_methods(person_image, shirt_image)
        test_transformation_options(person_image, shirt_image)
    
    if os.path.exists(person_image) and os.path.exists(pants_image):
        test_warp_cloth(person_image, pants_image, 'pants')
        test_warp_pants(person_image, pants_image)
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
    print("\nNote: For full testing, provide:")
    print("  - test_person.jpg (person in standing pose)")
    print("  - test_shirt.jpg (shirt/top clothing)")
    print("  - test_pants.jpg (pants/bottom clothing)")
    print("\nOr modify the paths in this script to use your images.")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Please ensure the server is running:")
        print("  python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
