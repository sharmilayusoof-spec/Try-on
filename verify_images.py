"""
Verify all clothing images exist and are valid
"""
import os
import json
from PIL import Image

def verify_images():
    """Check that all images referenced in clothes.json exist"""
    
    print("="*60)
    print("IMAGE VERIFICATION")
    print("="*60)
    
    # Load clothes.json
    json_path = 'frontend/assets/clothes/clothes.json'
    
    if not os.path.exists(json_path):
        print(f"❌ {json_path} not found!")
        return False
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    clothes = data.get('clothes', [])
    print(f"\n📋 Found {len(clothes)} items in clothes.json\n")
    
    all_ok = True
    
    for item in clothes:
        item_id = item.get('id')
        name = item.get('name')
        image = item.get('image')
        
        print(f"Checking: {name} ({item_id})")
        
        # Check if image file exists
        image_path = f'frontend/assets/clothes/{image}'
        
        if not os.path.exists(image_path):
            print(f"  ❌ Image missing: {image}")
            all_ok = False
            continue
        
        # Check if it's a valid image
        try:
            img = Image.open(image_path)
            width, height = img.size
            format_type = img.format
            print(f"  ✅ {image} - {width}x{height} {format_type}")
        except Exception as e:
            print(f"  ❌ Invalid image: {e}")
            all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ ALL IMAGES VERIFIED!")
        print("="*60)
        print("\nYour images are ready to use!")
        print("\nNext steps:")
        print("1. Open frontend/index.html in browser")
        print("2. Check that clothing grid shows images")
        print("3. Verify no 404 errors in console (F12)")
        print("\nTo use real images:")
        print("- Replace placeholder images with real clothing photos")
        print("- Keep same filenames (shirt1.png, pants1.png, etc.)")
        print("- Recommended size: 512x512 or 1024x1024 pixels")
    else:
        print("❌ SOME IMAGES MISSING OR INVALID")
        print("="*60)
        print("\nRun this to create missing images:")
        print("  python create_placeholder_images.py")
    
    print()
    return all_ok


if __name__ == "__main__":
    verify_images()
