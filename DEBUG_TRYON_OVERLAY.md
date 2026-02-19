# Virtual Try-On Overlay Debugging Guide

## Problem Analysis

**Symptom:** Cloth not appearing in final output despite successful upload and processing.

**Root Cause Analysis:** Based on code review, the issue is likely in one of these areas:

1. **Mask is all zeros** (most common)
2. **Warped cloth is transparent/black**
3. **Coordinate mismatch between images**
4. **Alpha channel issue**
5. **Overlay not being called**

---

## Step-by-Step Debugging

### STAGE 1: Verify Mask Generation

**Problem:** If the cloth mask is all zeros, nothing will be overlaid.

**Check:**
```python
# Add to overlay_engine.py in overlay_cloth() method, after line 60:

# DEBUG: Check mask
mask_sum = np.sum(cloth_mask)
mask_nonzero = np.count_nonzero(cloth_mask)
print(f"[DEBUG] Mask sum: {mask_sum}, Non-zero pixels: {mask_nonzero}")
print(f"[DEBUG] Mask shape: {cloth_mask.shape}, dtype: {cloth_mask.dtype}")
print(f"[DEBUG] Mask min: {cloth_mask.min()}, max: {cloth_mask.max()}")

# Save mask for visual inspection
cv2.imwrite('/tmp/debug_mask.png', cloth_mask)
```

**Expected Output:**
```
[DEBUG] Mask sum: 5000000+, Non-zero pixels: 50000+
[DEBUG] Mask shape: (512, 512), dtype: uint8
[DEBUG] Mask min: 0, max: 255
```

**If mask is all zeros:**
```
[DEBUG] Mask sum: 0, Non-zero pixels: 0  ← PROBLEM!
```

**Fix:** The mask generation is failing. Check segmentation output.

---

### STAGE 2: Verify Warped Cloth

**Problem:** Warped cloth might be black/transparent.

**Check:**
```python
# Add to overlay_engine.py in overlay_cloth() method, after line 60:

# DEBUG: Check cloth image
cloth_mean = np.mean(cloth_image)
cloth_nonzero = np.count_nonzero(cloth_image)
print(f"[DEBUG] Cloth mean intensity: {cloth_mean}")
print(f"[DEBUG] Cloth non-zero pixels: {cloth_nonzero}")
print(f"[DEBUG] Cloth shape: {cloth_image.shape}, dtype: {cloth_image.dtype}")

# Save cloth for visual inspection
cv2.imwrite('/tmp/debug_cloth.png', cloth_image)
```

**Expected Output:**
```
[DEBUG] Cloth mean intensity: 100-150
[DEBUG] Cloth non-zero pixels: 200000+
[DEBUG] Cloth shape: (512, 512, 3), dtype: uint8
```

**If cloth is black:**
```
[DEBUG] Cloth mean intensity: 0-10  ← PROBLEM!
```

**Fix:** Warping is producing black output. Check warping stage.

---

### STAGE 3: Verify Size Matching

**Problem:** Images might have size mismatch.

**Check:**
```python
# Add to overlay_engine.py in overlay_cloth() method, after line 60:

# DEBUG: Check sizes
print(f"[DEBUG] Person shape: {person_image.shape}")
print(f"[DEBUG] Cloth shape: {cloth_image.shape}")
print(f"[DEBUG] Mask shape: {cloth_mask.shape}")

if cloth_image.shape[:2] != person_image.shape[:2]:
    print(f"[DEBUG] SIZE MISMATCH! Resizing cloth...")
```

**Expected:** All should have same height and width.

---

### STAGE 4: Verify Alpha Blending

**Problem:** Alpha blending might not be working correctly.

**Check in `alpha_blending.py` blend() method:**

```python
# Add after line 50 in alpha_blending.py:

# DEBUG: Check alpha channel
print(f"[DEBUG] Alpha channel shape: {alpha_channel.shape}")
print(f"[DEBUG] Alpha channel min: {alpha_channel.min()}, max: {alpha_channel.max()}")
print(f"[DEBUG] Alpha channel mean: {alpha_channel.mean()}")

# Save alpha channel
alpha_vis = (alpha_channel * 255).astype(np.uint8)
if len(alpha_vis.shape) == 3:
    alpha_vis = alpha_vis[:, :, 0]
cv2.imwrite('/tmp/debug_alpha.png', alpha_vis)

# DEBUG: Check blending
print(f"[DEBUG] Background shape: {bg.shape}, dtype: {bg.dtype}")
print(f"[DEBUG] Foreground shape: {fg.shape}, dtype: {fg.dtype}")
print(f"[DEBUG] Blended mean: {blended.mean()}")

# Save intermediate result
cv2.imwrite('/tmp/debug_blended.png', result)
```

---

## Most Likely Issues & Fixes

### Issue 1: Mask is All Zeros (90% probability)

**Cause:** Segmentation not generating proper mask OR mask not being passed correctly.

**Detection:**
```python
if np.count_nonzero(cloth_mask) == 0:
    print("ERROR: Mask is all zeros!")
```

**Fix Option A - Generate Simple Mask:**
```python
# Add to overlay_engine.py, before overlay_cloth() blending:

# If mask is empty, create one from cloth image
if np.count_nonzero(cloth_mask) == 0:
    print("[FIX] Generating mask from cloth image...")
    # Convert cloth to grayscale
    gray = cv2.cvtColor(cloth_image, cv2.COLOR_BGR2GRAY)
    # Threshold to create mask (assuming white/light background)
    _, cloth_mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    # Clean up mask
    kernel = np.ones((5,5), np.uint8)
    cloth_mask = cv2.morphologyEx(cloth_mask, cv2.MORPH_CLOSE, kernel)
    cloth_mask = cv2.morphologyEx(cloth_mask, cv2.MORPH_OPEN, kernel)
```

**Fix Option B - Use Full Mask:**
```python
# If mask is empty, use full opacity
if np.count_nonzero(cloth_mask) == 0:
    print("[FIX] Using full mask...")
    cloth_mask = np.ones(cloth_image.shape[:2], dtype=np.uint8) * 255
```

---

### Issue 2: Warped Cloth is Black

**Cause:** Warping producing invalid output.

**Detection:**
```python
if np.mean(cloth_image) < 10:
    print("ERROR: Warped cloth is black!")
```

**Fix - Check Warping Output:**
```python
# In warping.py, after warping (line ~100):

# Verify warped output
if np.mean(warped) < 10:
    print("[ERROR] Warping produced black image!")
    print(f"Source points: {source_pts}")
    print(f"Target points: {target_pts}")
    # Use original cloth as fallback
    warped = cloth_img.copy()
```

---

### Issue 3: Alpha Channel Not Applied

**Cause:** Alpha channel calculation error in blend() method.

**Detection:**
```python
if alpha_channel.max() == 0:
    print("ERROR: Alpha channel is all zeros!")
```

**Fix in `alpha_blending.py`:**

```python
# Replace lines 40-50 in alpha_blending.py with:

# Get alpha channel
if foreground.shape[2] == 4:
    # Use existing alpha
    alpha_channel = fg[:, :, 3:4]
    fg = fg[:, :, :3]
elif mask is not None:
    # Use mask as alpha
    if len(mask.shape) == 2:
        alpha_channel = mask.astype(np.float32) / 255.0
        alpha_channel = alpha_channel[:, :, np.newaxis]
    else:
        alpha_channel = mask.astype(np.float32) / 255.0
        if alpha_channel.shape[2] > 1:
            alpha_channel = alpha_channel[:, :, 0:1]
    
    # CRITICAL FIX: Ensure alpha is not all zeros
    if np.max(alpha_channel) == 0:
        print("[WARNING] Mask is all zeros, using full opacity")
        alpha_channel = np.ones((fg.shape[0], fg.shape[1], 1), dtype=np.float32)
else:
    # Full opacity
    alpha_channel = np.ones((fg.shape[0], fg.shape[1], 1), dtype=np.float32)
```

---

### Issue 4: Blend Result Not Saved

**Cause:** Result computed but not returned/saved properly.

**Fix in `overlay_engine.py`:**

```python
# Add at the end of overlay_cloth() method, before return:

# DEBUG: Verify result is different from input
diff = cv2.absdiff(result, person_image)
diff_sum = np.sum(diff)
print(f"[DEBUG] Difference from original: {diff_sum}")

if diff_sum < 1000:
    print("[WARNING] Result is almost identical to input!")
    print("[WARNING] Overlay may not have been applied!")

# Save result for inspection
cv2.imwrite('/tmp/debug_result.png', result)
```

---

## Complete Fix - Add to overlay_engine.py

**Add this comprehensive fix to the `overlay_cloth()` method:**

```python
def overlay_cloth(
    self,
    person_image: np.ndarray,
    cloth_image: np.ndarray,
    cloth_mask: np.ndarray,
    method: str = 'alpha',
    match_colors: bool = True,
    add_shadow: bool = True,
    feather_edges: bool = True,
    shadow_intensity: float = 0.3,
    alpha: float = 1.0
) -> Tuple[np.ndarray, Dict]:
    """Overlay cloth onto person with all enhancements."""
    
    # ============ DEBUGGING SECTION ============
    print("\n=== OVERLAY DEBUG INFO ===")
    print(f"Person shape: {person_image.shape}")
    print(f"Cloth shape: {cloth_image.shape}")
    print(f"Mask shape: {cloth_mask.shape}")
    print(f"Mask non-zero pixels: {np.count_nonzero(cloth_mask)}")
    print(f"Cloth mean intensity: {np.mean(cloth_image):.2f}")
    
    # CRITICAL FIX 1: Check if mask is empty
    if np.count_nonzero(cloth_mask) == 0:
        print("[CRITICAL] Mask is all zeros! Generating mask from cloth...")
        gray = cv2.cvtColor(cloth_image, cv2.COLOR_BGR2GRAY)
        _, cloth_mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5,5), np.uint8)
        cloth_mask = cv2.morphologyEx(cloth_mask, cv2.MORPH_CLOSE, kernel)
        print(f"Generated mask non-zero pixels: {np.count_nonzero(cloth_mask)}")
    
    # CRITICAL FIX 2: Check if cloth is black
    if np.mean(cloth_image) < 10:
        print("[CRITICAL] Cloth image is black! This will produce no visible output.")
        # Could load original cloth here as fallback
    
    # Save debug images
    cv2.imwrite('/tmp/debug_person.png', person_image)
    cv2.imwrite('/tmp/debug_cloth.png', cloth_image)
    cv2.imwrite('/tmp/debug_mask.png', cloth_mask)
    # ============ END DEBUGGING ============
    
    metadata = {
        'method': method,
        'color_matched': match_colors,
        'shadow_added': add_shadow,
        'edges_feathered': feather_edges
    }
    
    # Ensure same size
    if cloth_image.shape[:2] != person_image.shape[:2]:
        cloth_image = cv2.resize(
            cloth_image,
            (person_image.shape[1], person_image.shape[0])
        )
    
    if cloth_mask.shape[:2] != person_image.shape[:2]:
        cloth_mask = cv2.resize(
            cloth_mask,
            (person_image.shape[1], person_image.shape[0])
        )
    
    # Color matching
    if match_colors:
        cloth_image = self.color_matcher.match_histogram(
            cloth_image,
            person_image,
            cloth_mask
        )
    
    # Add shadow to background
    result = person_image.copy()
    if add_shadow:
        shadow = self.shadow_generator.generate_shadow(
            cloth_mask,
            intensity=shadow_intensity,
            blur_amount=15,
            offset=(5, 5)
        )
        result = self.shadow_generator.apply_shadow(result, shadow)
    
    # Feather edges
    blend_mask = cloth_mask
    if feather_edges:
        blend_mask = self.alpha_blender._feather_mask(cloth_mask, 10)
    
    # Apply overlay method
    if method == 'alpha':
        result = self.alpha_blender.blend(
            result,
            cloth_image,
            blend_mask,
            alpha
        )
    elif method == 'seamless':
        try:
            result = self.seamless_cloner.clone(
                cloth_image,
                result,
                cloth_mask,
                method='normal'
            )
        except Exception as e:
            logger.warning(f"Seamless cloning failed: {e}, using alpha blend")
            result = self.alpha_blender.blend(
                result,
                cloth_image,
                blend_mask,
                alpha
            )
    elif method == 'mixed':
        try:
            result = self.seamless_cloner.clone(
                cloth_image,
                result,
                cloth_mask,
                method='mixed'
            )
        except Exception as e:
            logger.warning(f"Mixed cloning failed: {e}, using alpha blend")
            result = self.alpha_blender.blend(
                result,
                cloth_image,
                blend_mask,
                alpha
            )
    else:
        raise ValueError(f"Unknown overlay method: {method}")
    
    # ============ FINAL VERIFICATION ============
    diff = cv2.absdiff(result, person_image)
    diff_sum = np.sum(diff)
    print(f"Difference from original: {diff_sum}")
    
    if diff_sum < 1000:
        print("[WARNING] Result almost identical to input - overlay may have failed!")
    
    cv2.imwrite('/tmp/debug_result.png', result)
    print("=== END OVERLAY DEBUG ===\n")
    # ============ END VERIFICATION ============
    
    return result, metadata
```

---

## Quick Test Script

Create `test_overlay.py` in the backend root:

```python
import cv2
import numpy as np
from app.services.ml.overlay_engine import OverlayEngine

# Load test images
person = cv2.imread('path/to/person.jpg')
cloth = cv2.imread('path/to/cloth.jpg')

# Create a simple test mask
mask = np.ones(cloth.shape[:2], dtype=np.uint8) * 255

# Test overlay
engine = OverlayEngine()
result, metadata = engine.overlay_cloth(
    person,
    cloth,
    mask,
    method='alpha'
)

# Save result
cv2.imwrite('test_result.jpg', result)
print("Test complete. Check test_result.jpg")
```

Run:
```bash
python test_overlay.py
```

---

## Expected Debug Output (Working System)

```
=== OVERLAY DEBUG INFO ===
Person shape: (512, 512, 3)
Cloth shape: (512, 512, 3)
Mask shape: (512, 512)
Mask non-zero pixels: 65536
Cloth mean intensity: 127.45
Difference from original: 15000000
=== END OVERLAY DEBUG ===
```

## Expected Debug Output (Broken System)

```
=== OVERLAY DEBUG INFO ===
Person shape: (512, 512, 3)
Cloth shape: (512, 512, 3)
Mask shape: (512, 512)
Mask non-zero pixels: 0  ← PROBLEM!
Cloth mean intensity: 127.45
[CRITICAL] Mask is all zeros! Generating mask from cloth...
Generated mask non-zero pixels: 45000
Difference from original: 12000000
=== END OVERLAY DEBUG ===
```

---

## Summary of Fixes

1. **Add mask validation** - Check if mask is all zeros
2. **Add mask generation fallback** - Create mask from cloth if needed
3. **Add cloth validation** - Check if cloth is black
4. **Add debug logging** - Print all intermediate values
5. **Add debug image saving** - Save all intermediate images to /tmp/
6. **Add result verification** - Check if result differs from input

Apply these fixes and run your try-on again. The debug output will tell you exactly where the problem is!

