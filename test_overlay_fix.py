"""
Test script to verify overlay fix

This script tests the overlay functionality with debug output.
Run this to diagnose overlay issues.
"""
import cv2
import numpy as np
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.ml.overlay_engine import OverlayEngine


def create_test_images():
    """Create simple test images for debugging"""
    # Create person image (blue background)
    person = np.zeros((512, 512, 3), dtype=np.uint8)
    person[:, :] = [200, 150, 100]  # Brownish color
    
    # Add a simple "body" shape
    cv2.rectangle(person, (150, 100), (350, 450), (180, 140, 100), -1)
    
    # Create cloth image (red shirt)
    cloth = np.zeros((512, 512, 3), dtype=np.uint8)
    cloth[:, :] = [50, 50, 200]  # Red color
    
    # Create cloth mask (shirt shape)
    mask = np.zeros((512, 512), dtype=np.uint8)
    cv2.rectangle(mask, (150, 100), (350, 300), 255, -1)
    
    return person, cloth, mask


def test_with_real_images(person_path, cloth_path, mask_path=None):
    """Test with real images"""
    print("\n" + "="*60)
    print("TESTING WITH REAL IMAGES")
    print("="*60)
    
    # Load images
    person = cv2.imread(person_path)
    cloth = cv2.imread(cloth_path)
    
    if person is None:
        print(f"ERROR: Could not load person image: {person_path}")
        return
    
    if cloth is None:
        print(f"ERROR: Could not load cloth image: {cloth_path}")
        return
    
    print(f"Loaded person: {person.shape}")
    print(f"Loaded cloth: {cloth.shape}")
    
    # Load or create mask
    if mask_path and os.path.exists(mask_path):
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        print(f"Loaded mask: {mask.shape}")
    else:
        print("No mask provided, will be auto-generated")
        mask = np.zeros(cloth.shape[:2], dtype=np.uint8)
    
    # Test overlay
    engine = OverlayEngine()
    result, metadata = engine.overlay_cloth(
        person,
        cloth,
        mask,
        method='alpha',
        match_colors=True,
        add_shadow=True,
        feather_edges=True
    )
    
    # Save result
    output_path = 'test_overlay_result.jpg'
    cv2.imwrite(output_path, result)
    print(f"\n✓ Result saved to: {output_path}")
    print(f"✓ Metadata: {metadata}")
    
    return result


def test_with_synthetic_images():
    """Test with synthetic images"""
    print("\n" + "="*60)
    print("TESTING WITH SYNTHETIC IMAGES")
    print("="*60)
    
    # Create test images
    person, cloth, mask = create_test_images()
    
    print(f"Created person: {person.shape}")
    print(f"Created cloth: {cloth.shape}")
    print(f"Created mask: {mask.shape}, non-zero: {np.count_nonzero(mask)}")
    
    # Save test inputs
    cv2.imwrite('test_person.png', person)
    cv2.imwrite('test_cloth.png', cloth)
    cv2.imwrite('test_mask.png', mask)
    print("✓ Test inputs saved")
    
    # Test overlay
    engine = OverlayEngine()
    result, metadata = engine.overlay_cloth(
        person,
        cloth,
        mask,
        method='alpha',
        match_colors=False,  # Skip for synthetic
        add_shadow=True,
        feather_edges=True
    )
    
    # Save result
    cv2.imwrite('test_synthetic_result.jpg', result)
    print(f"\n✓ Result saved to: test_synthetic_result.jpg")
    print(f"✓ Metadata: {metadata}")
    
    # Verify result
    diff = cv2.absdiff(result, person)
    diff_sum = np.sum(diff)
    
    print(f"\nVerification:")
    print(f"  Difference sum: {diff_sum:,.0f}")
    
    if diff_sum > 10000:
        print("  ✓ SUCCESS: Overlay applied (significant difference detected)")
    else:
        print("  ✗ FAILURE: No visible overlay (difference too small)")
    
    return result


def test_empty_mask():
    """Test with empty mask (common failure case)"""
    print("\n" + "="*60)
    print("TESTING WITH EMPTY MASK (Common Failure Case)")
    print("="*60)
    
    # Create test images
    person, cloth, _ = create_test_images()
    
    # Create EMPTY mask (all zeros)
    mask = np.zeros((512, 512), dtype=np.uint8)
    
    print(f"Created person: {person.shape}")
    print(f"Created cloth: {cloth.shape}")
    print(f"Created EMPTY mask: {mask.shape}, non-zero: {np.count_nonzero(mask)}")
    print("This should trigger the auto-fix!")
    
    # Test overlay
    engine = OverlayEngine()
    result, metadata = engine.overlay_cloth(
        person,
        cloth,
        mask,
        method='alpha',
        match_colors=False,
        add_shadow=False,
        feather_edges=False
    )
    
    # Save result
    cv2.imwrite('test_empty_mask_result.jpg', result)
    print(f"\n✓ Result saved to: test_empty_mask_result.jpg")
    
    # Verify result
    diff = cv2.absdiff(result, person)
    diff_sum = np.sum(diff)
    
    print(f"\nVerification:")
    print(f"  Difference sum: {diff_sum:,.0f}")
    
    if diff_sum > 10000:
        print("  ✓ SUCCESS: Auto-fix worked! Overlay applied despite empty mask")
    else:
        print("  ✗ FAILURE: Auto-fix did not work")
    
    return result


def main():
    """Main test function"""
    print("\n" + "="*60)
    print("OVERLAY FIX TEST SCRIPT")
    print("="*60)
    
    # Test 1: Synthetic images
    print("\n[TEST 1] Synthetic images with valid mask")
    test_with_synthetic_images()
    
    # Test 2: Empty mask (common failure)
    print("\n[TEST 2] Empty mask (should auto-fix)")
    test_empty_mask()
    
    # Test 3: Real images (if provided)
    if len(sys.argv) >= 3:
        person_path = sys.argv[1]
        cloth_path = sys.argv[2]
        mask_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        print("\n[TEST 3] Real images")
        test_with_real_images(person_path, cloth_path, mask_path)
    else:
        print("\n[TEST 3] Skipped (no real images provided)")
        print("Usage: python test_overlay_fix.py <person.jpg> <cloth.jpg> [mask.png]")
    
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60)
    print("\nCheck the following files:")
    print("  - test_synthetic_result.jpg")
    print("  - test_empty_mask_result.jpg")
    print("  - /tmp/tryon_debug/ (debug images)")
    print("\nIf overlay is still not visible, check:")
    print("  1. Mask generation (should auto-fix if empty)")
    print("  2. Cloth image (should not be black)")
    print("  3. Debug images in /tmp/tryon_debug/")


if __name__ == '__main__':
    main()
