"""
Test script for overlay endpoints
"""
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"


def test_overlay_info():
    """Test overlay info endpoint"""
    print("\n=== Testing Overlay Info ===")
    
    response = requests.get(f"{BASE_URL}/overlay/overlay-info")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Overlay info retrieved")
        print(f"Available methods: {list(data['methods'].keys())}")
        print(f"Features: {list(data['features'].keys())}")
        print(f"Quick overlay time: {data['performance']['total_quick']}")
        print(f"HQ overlay time: {data['performance']['total_high_quality']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_overlay(person_path: str, cloth_path: str, mask_path: str):
    """Test general overlay endpoint"""
    print("\n=== Testing General Overlay ===")
    
    if not all(os.path.exists(p) for p in [person_path, cloth_path, mask_path]):
        print("❌ One or more images not found")
        return
    
    with open(person_path, 'rb') as pf, \
         open(cloth_path, 'rb') as cf, \
         open(mask_path, 'rb') as mf:
        
        files = {
            'person_image': ('person.jpg', pf, 'image/jpeg'),
            'cloth_image': ('cloth.jpg', cf, 'image/jpeg'),
            'cloth_mask': ('mask.png', mf, 'image/png')
        }
        
        params = {
            'method': 'alpha',
            'match_colors': True,
            'add_shadow': True,
            'feather_edges': True,
            'shadow_intensity': 0.3,
            'alpha': 1.0
        }
        
        response = requests.post(
            f"{BASE_URL}/overlay/overlay",
            files=files,
            params=params
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Overlay completed")
        print(f"File ID: {data['file_id']}")
        print(f"Method: {data['metadata']['method']}")
        print(f"Color matched: {data['metadata']['color_matched']}")
        print(f"Shadow added: {data['metadata']['shadow_added']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_quick_overlay(person_path: str, cloth_path: str, mask_path: str):
    """Test quick overlay"""
    print("\n=== Testing Quick Overlay ===")
    
    if not all(os.path.exists(p) for p in [person_path, cloth_path, mask_path]):
        print("❌ One or more images not found")
        return
    
    with open(person_path, 'rb') as pf, \
         open(cloth_path, 'rb') as cf, \
         open(mask_path, 'rb') as mf:
        
        files = {
            'person_image': ('person.jpg', pf, 'image/jpeg'),
            'cloth_image': ('cloth.jpg', cf, 'image/jpeg'),
            'cloth_mask': ('mask.png', mf, 'image/png')
        }
        
        response = requests.post(
            f"{BASE_URL}/overlay/quick-overlay",
            files=files
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Quick overlay completed")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_high_quality_overlay(person_path: str, cloth_path: str, mask_path: str, body_mask_path: str = None):
    """Test high-quality overlay"""
    print("\n=== Testing High-Quality Overlay ===")
    
    if not all(os.path.exists(p) for p in [person_path, cloth_path, mask_path]):
        print("❌ One or more images not found")
        return
    
    files = {}
    
    with open(person_path, 'rb') as pf, \
         open(cloth_path, 'rb') as cf, \
         open(mask_path, 'rb') as mf:
        
        files['person_image'] = ('person.jpg', pf.read(), 'image/jpeg')
        files['cloth_image'] = ('cloth.jpg', cf.read(), 'image/jpeg')
        files['cloth_mask'] = ('mask.png', mf.read(), 'image/png')
        
        if body_mask_path and os.path.exists(body_mask_path):
            with open(body_mask_path, 'rb') as bmf:
                files['body_mask'] = ('body_mask.png', bmf.read(), 'image/png')
        
        response = requests.post(
            f"{BASE_URL}/overlay/high-quality-overlay",
            files=files
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ High-quality overlay completed")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_overlay_methods(person_path: str, cloth_path: str, mask_path: str):
    """Test different overlay methods"""
    print("\n=== Testing Overlay Methods ===")
    
    methods = ['alpha', 'seamless', 'mixed']
    
    for method in methods:
        print(f"\nTesting {method.upper()} method...")
        
        if not all(os.path.exists(p) for p in [person_path, cloth_path, mask_path]):
            print("❌ Images not found")
            continue
        
        with open(person_path, 'rb') as pf, \
             open(cloth_path, 'rb') as cf, \
             open(mask_path, 'rb') as mf:
            
            files = {
                'person_image': ('person.jpg', pf, 'image/jpeg'),
                'cloth_image': ('cloth.jpg', cf, 'image/jpeg'),
                'cloth_mask': ('mask.png', mf, 'image/png')
            }
            
            response = requests.post(
                f"{BASE_URL}/overlay/overlay",
                files=files,
                params={'method': method}
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {method.upper()} overlay successful")
            print(f"   File ID: {data['file_id']}")
        else:
            print(f"❌ {method.upper()} failed: {response.status_code}")


def test_color_matching(cloth_path: str, reference_path: str):
    """Test color matching"""
    print("\n=== Testing Color Matching ===")
    
    if not os.path.exists(cloth_path) or not os.path.exists(reference_path):
        print("❌ Images not found")
        return
    
    with open(cloth_path, 'rb') as cf, \
         open(reference_path, 'rb') as rf:
        
        files = {
            'cloth_image': ('cloth.jpg', cf, 'image/jpeg'),
            'reference_image': ('reference.jpg', rf, 'image/jpeg')
        }
        
        response = requests.post(
            f"{BASE_URL}/overlay/match-colors",
            files=files
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Color matching completed")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_shadow_generation(image_path: str, mask_path: str):
    """Test shadow generation"""
    print("\n=== Testing Shadow Generation ===")
    
    if not os.path.exists(image_path) or not os.path.exists(mask_path):
        print("❌ Images not found")
        return
    
    with open(image_path, 'rb') as imgf, \
         open(mask_path, 'rb') as mf:
        
        files = {
            'image': ('image.jpg', imgf, 'image/jpeg'),
            'mask': ('mask.png', mf, 'image/png')
        }
        
        params = {
            'intensity': 0.3,
            'blur_amount': 15,
            'offset_x': 5,
            'offset_y': 5
        }
        
        response = requests.post(
            f"{BASE_URL}/overlay/add-shadow",
            files=files,
            params=params
        )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Shadow added successfully")
        print(f"File ID: {data['file_id']}")
        print(f"URL: {data['url']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_overlay_options(person_path: str, cloth_path: str, mask_path: str):
    """Test different overlay options"""
    print("\n=== Testing Overlay Options ===")
    
    options = [
        {'name': 'Full features', 'match_colors': True, 'add_shadow': True, 'feather_edges': True},
        {'name': 'No color match', 'match_colors': False, 'add_shadow': True, 'feather_edges': True},
        {'name': 'No shadow', 'match_colors': True, 'add_shadow': False, 'feather_edges': True},
        {'name': 'No feather', 'match_colors': True, 'add_shadow': True, 'feather_edges': False},
        {'name': 'Minimal', 'match_colors': False, 'add_shadow': False, 'feather_edges': False}
    ]
    
    for opt in options:
        print(f"\nTesting {opt['name']}...")
        
        if not all(os.path.exists(p) for p in [person_path, cloth_path, mask_path]):
            print("❌ Images not found")
            continue
        
        with open(person_path, 'rb') as pf, \
             open(cloth_path, 'rb') as cf, \
             open(mask_path, 'rb') as mf:
            
            files = {
                'person_image': ('person.jpg', pf, 'image/jpeg'),
                'cloth_image': ('cloth.jpg', cf, 'image/jpeg'),
                'cloth_mask': ('mask.png', mf, 'image/png')
            }
            
            params = {
                'method': 'alpha',
                'match_colors': opt['match_colors'],
                'add_shadow': opt['add_shadow'],
                'feather_edges': opt['feather_edges']
            }
            
            response = requests.post(
                f"{BASE_URL}/overlay/overlay",
                files=files,
                params=params
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {opt['name']} successful")
            print(f"   Metadata: {data['metadata']}")
        else:
            print(f"❌ Failed: {response.status_code}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("OVERLAY MODULE TEST SUITE")
    print("=" * 60)
    
    # Test info endpoint (no images needed)
    test_overlay_info()
    
    # Define test image paths
    person_image = "test_person.jpg"
    cloth_image = "test_cloth.jpg"
    mask_image = "test_mask.png"
    body_mask_image = "test_body_mask.png"
    
    # Check if test images exist
    print("\n=== Checking Test Images ===")
    if os.path.exists(person_image):
        print(f"✅ Person image found: {person_image}")
    else:
        print(f"⚠️  Person image not found: {person_image}")
    
    if os.path.exists(cloth_image):
        print(f"✅ Cloth image found: {cloth_image}")
    else:
        print(f"⚠️  Cloth image not found: {cloth_image}")
    
    if os.path.exists(mask_image):
        print(f"✅ Mask image found: {mask_image}")
    else:
        print(f"⚠️  Mask image not found: {mask_image}")
    
    # Run tests if images exist
    if all(os.path.exists(p) for p in [person_image, cloth_image, mask_image]):
        test_overlay(person_image, cloth_image, mask_image)
        test_quick_overlay(person_image, cloth_image, mask_image)
        test_high_quality_overlay(person_image, cloth_image, mask_image, body_mask_image)
        test_overlay_methods(person_image, cloth_image, mask_image)
        test_overlay_options(person_image, cloth_image, mask_image)
        test_color_matching(cloth_image, person_image)
        test_shadow_generation(person_image, mask_image)
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)
    print("\nNote: For full testing, provide:")
    print("  - test_person.jpg (person image)")
    print("  - test_cloth.jpg (warped cloth image)")
    print("  - test_mask.png (cloth mask)")
    print("  - test_body_mask.png (optional body mask)")
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
