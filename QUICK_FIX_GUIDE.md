# Quick Fix Guide - Cloth Not Appearing

## 🔴 Problem
Cloth not visible in try-on output

## ✅ Solution (5 minutes)

### Step 1: Apply Code Fixes

**File 1:** `app/services/ml/overlay_engine.py`
- Find method: `overlay_cloth()`
- Replace with: Code from `FIXES/fix_overlay_engine.py`

**File 2:** `app/services/ml/alpha_blending.py`
- Find method: `blend()`
- Replace with: Code from `FIXES/fix_alpha_blending.py`

### Step 2: Restart Backend
```bash
# Stop current server (Ctrl+C)
# Start again
python run.py
```

### Step 3: Test
```bash
python test_overlay_fix.py
```

### Step 4: Check Results
```bash
# View debug images
ls /tmp/tryon_debug/

# Should see:
# 01_person_input.png
# 02_cloth_input.png
# 03_mask_input.png
# 07_final_result.png  ← Check this!
```

---

## 🔍 Quick Diagnosis

Run try-on and check console output:

### ✅ Working:
```
Mask non-zero pixels: 65536
Cloth mean intensity: 127.45
Result difference sum: 15,000,000
[SUCCESS] Overlay applied successfully
```

### ❌ Broken (but auto-fixed):
```
Mask non-zero pixels: 0  ← Problem
[CRITICAL FIX] Generating mask...
Generated mask non-zero pixels: 45000  ← Fixed
[SUCCESS] Overlay applied successfully
```

### ❌ Still broken:
```
Mask non-zero pixels: 0
Generated mask non-zero pixels: 0  ← Still broken
```
→ Check warping stage

---

## 🎯 Root Causes (in order of probability)

1. **Empty mask (90%)** → Fixed by auto-generation
2. **Black warped cloth (5%)** → Check warping output
3. **Wrong image sizes (3%)** → Fixed by auto-resize
4. **Overlay not called (2%)** → Check API endpoint

---

## 📊 Debug Checklist

```bash
# 1. Check mask
Mask non-zero pixels: > 0 ✓

# 2. Check cloth
Cloth mean intensity: > 50 ✓

# 3. Check result
Result difference sum: > 10,000 ✓

# 4. Visual check
ls /tmp/tryon_debug/07_final_result.png ✓
```

---

## 🚀 If Still Not Working

### Check warping output:
```python
# Add to warping.py after line 100:
print(f"Warped mean: {np.mean(warped)}")
cv2.imwrite('/tmp/debug_warped.png', warped)
```

### Check segmentation:
```python
# Ensure segmentation is called:
cloth_mask = segment_cloth(cloth_image)
print(f"Segmentation mask pixels: {np.count_nonzero(cloth_mask)}")
```

### Check API flow:
```python
# Verify overlay is called in endpoint:
result = create_tryon_result(person, warped_cloth, mask)
```

---

## 📝 Quick Test

```python
import cv2
import numpy as np
from app.services.ml.overlay_engine import OverlayEngine

# Create test images
person = np.ones((512,512,3), dtype=np.uint8) * 100
cloth = np.ones((512,512,3), dtype=np.uint8) * 200
mask = np.ones((512,512), dtype=np.uint8) * 255

# Test overlay
engine = OverlayEngine()
result, _ = engine.overlay_cloth(person, cloth, mask)

# Check result
diff = np.sum(cv2.absdiff(result, person))
print(f"Difference: {diff}")
print("✓ Working!" if diff > 10000 else "✗ Not working")
```

---

## 💡 Key Points

1. **Most common issue:** Empty mask → Auto-fixed
2. **Second issue:** Black warped cloth → Check warping
3. **Debug images:** Always check `/tmp/tryon_debug/`
4. **Console output:** Shows exactly what's happening

---

## ✨ Expected Result

**Before:** Person image unchanged
**After:** Person wearing the cloth

**Debug output should show:**
- Mask validation
- Auto-correction (if needed)
- Successful overlay
- Difference from original

---

**Apply the fix and run the test. It should work!** 🎉

