# Frontend-Backend Connection Issue - Diagnosis & Fix

## 🔴 Problem Identified

**Frontend is trying to connect to:** `http://localhost:8000/api/v1/tryon/process`  
**Backend endpoint that exists:** `http://localhost:8000/api/v1/tryon/try-on`

**ROOT CAUSE: URL Path Mismatch** ❌

---

## 🔍 Issues Found

### Issue 1: Wrong Endpoint Path (CRITICAL)
**Frontend calls:** `/api/v1/tryon/process`  
**Backend has:** `/api/v1/tryon/try-on`

### Issue 2: Endpoint Not Implemented
The `/try-on` endpoint exists but returns 501 (Not Implemented)

### Issue 3: CORS Configuration
Backend only allows `http://localhost:3000` and `http://localhost:8000`  
If frontend runs on different port, CORS will block it

---

## ✅ Step-by-Step Diagnosis

### Step 1: Check if Backend is Running

```bash
# Test if backend is accessible
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2024-..."}
```

**If connection refused:**
- Backend is not running
- Wrong port
- Firewall blocking

**If 404:**
- Backend running but route doesn't exist

### Step 2: Check Available Endpoints

```bash
# List all endpoints
curl http://localhost:8000/docs

# Or check root
curl http://localhost:8000/

# Expected:
# {"message":"VTO Backend API","status":"active",...}
```

### Step 3: Check Exact Endpoint

```bash
# Test the endpoint frontend is calling
curl -X POST http://localhost:8000/api/v1/tryon/process

# Expected: 404 Not Found (endpoint doesn't exist)

# Test the actual endpoint
curl -X POST http://localhost:8000/api/v1/tryon/try-on

# Expected: 501 Not Implemented (endpoint exists but not ready)
```

### Step 4: Check CORS

```bash
# Test CORS from browser console
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

---

## 🔧 Fixes Required

### Fix 1: Update Frontend API URL (CRITICAL)

**File:** `frontend/script.js`

**Current (Line ~613):**
```javascript
const response = await fetch(`${CONFIG.apiBaseUrl}/api/v1/tryon/process`, {
```

**Fix Option A - Change to match backend:**
```javascript
const response = await fetch(`${CONFIG.apiBaseUrl}/api/v1/tryon/try-on`, {
```

**Fix Option B - Create the /process endpoint in backend** (see Fix 4)

---

### Fix 2: Update CORS to Allow Frontend Port

**File:** `app/core/config.py`

**Current (Line ~27):**
```python
ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
```

**Fix - Add common frontend ports:**
```python
ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8080"
```

Or if using file:// protocol:
```python
ALLOWED_ORIGINS: str = "*"  # Allow all (development only!)
```

---

### Fix 3: Implement the Try-On Endpoint

**File:** `app/api/v1/endpoints/tryon.py`

**Current:** Returns 501 Not Implemented

**Fix - Add a working endpoint:**

```python
from fastapi import APIRouter, HTTPException, status, File, UploadFile
from typing import Dict
import os
import cv2
import numpy as np

from app.core.config import settings
from app.utils.file_handler import generate_file_id, ensure_directory, get_file_url
from app.utils.image_processor import validate_and_read_image
from app.services.ml.pose_detection import detect_pose_from_image
from app.services.ml.cloth_warping import warp_cloth_to_body
from app.services.ml.control_points import ControlPointGenerator
from app.services.ml.overlay_engine import create_tryon_result

router = APIRouter()


@router.post(
    "/process",  # Add this endpoint
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Process virtual try-on",
    description="Upload user and clothing images to generate try-on result"
)
async def process_tryon(
    user_image: UploadFile = File(..., description="User photo"),
    cloth_image: UploadFile = File(..., description="Clothing image")
):
    """
    Process virtual try-on request.
    
    Complete implementation with all stages.
    """
    try:
        # Read images
        person_img, _ = await validate_and_read_image(user_image)
        cloth_img, _ = await validate_and_read_image(cloth_image)
        
        # Detect pose
        pose_result = detect_pose_from_image(person_img)
        
        if not pose_result.get('detected'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No pose detected in user image"
            )
        
        landmarks = pose_result['landmarks']
        
        # Generate control points for shirt
        generator = ControlPointGenerator()
        source_pts, target_pts = generator.generate_shirt_points(
            cloth_img.shape[:2],
            landmarks
        )
        
        # Add boundary points
        source_pts, target_pts = generator.add_boundary_points(
            source_pts,
            target_pts,
            cloth_img.shape[:2]
        )
        
        # Warp cloth
        warped_cloth = warp_cloth_to_body(
            cloth_img,
            source_pts,
            target_pts,
            person_img.shape[:2],
            method='tps'
        )
        
        # Create cloth mask
        gray = cv2.cvtColor(warped_cloth, cv2.COLOR_BGR2GRAY)
        _, cloth_mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        # Overlay
        result = create_tryon_result(
            person_img,
            warped_cloth,
            cloth_mask,
            quality='high'
        )
        
        # Save result
        file_id = generate_file_id("tryon_result")
        ensure_directory(settings.RESULTS_DIR)
        file_path = os.path.join(settings.RESULTS_DIR, f"{file_id}.jpg")
        cv2.imwrite(file_path, result)
        
        return {
            'status': 'success',
            'file_id': file_id,
            'image_url': get_file_url(file_path),
            'url': get_file_url(file_path),  # Alias for compatibility
            'message': 'Try-on completed successfully',
            'time_taken': 1.5  # Placeholder
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Try-on processing failed: {str(e)}"
        )


# Keep the old endpoint for compatibility
@router.post(
    "/try-on",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Process virtual try-on (alias)",
    description="Alias for /process endpoint"
)
async def process_tryon_alias(
    user_image: UploadFile = File(...),
    cloth_image: UploadFile = File(...)
):
    """Alias endpoint that calls the main process endpoint"""
    return await process_tryon(user_image, cloth_image)
```

---

### Fix 4: Add File URL Helper (if missing)

**File:** `app/utils/file_handler.py`

Add this function if it doesn't exist:

```python
def get_file_url(file_path: str) -> str:
    """
    Convert file path to URL.
    
    Args:
        file_path: Local file path
        
    Returns:
        URL path for the file
    """
    # Convert absolute path to relative URL
    if file_path.startswith(settings.RESULTS_DIR):
        relative_path = file_path.replace(settings.RESULTS_DIR, '/results')
        return relative_path
    elif file_path.startswith(settings.PROCESSED_DIR):
        relative_path = file_path.replace(settings.PROCESSED_DIR, '/processed')
        return relative_path
    elif file_path.startswith(settings.UPLOAD_DIR):
        relative_path = file_path.replace(settings.UPLOAD_DIR, '/uploads')
        return relative_path
    else:
        # Return as-is
        return file_path
```

---

## 🚀 Quick Fix (Minimal Changes)

### Option A: Fix Frontend Only (Fastest)

**File:** `frontend/script.js` (Line ~613)

```javascript
// Change this:
const response = await fetch(`${CONFIG.apiBaseUrl}/api/v1/tryon/process`, {

// To this:
const response = await fetch(`${CONFIG.apiBaseUrl}/api/v1/tryon/try-on`, {
```

**Note:** This will still get 501 error until endpoint is implemented.

---

### Option B: Fix Backend Only (Better)

**File:** `app/api/v1/endpoints/tryon.py`

Add the `/process` endpoint implementation (see Fix 3 above).

---

### Option C: Complete Fix (Recommended)

1. **Add `/process` endpoint to backend** (Fix 3)
2. **Update CORS** (Fix 2)
3. **Keep frontend as-is**

---

## 📋 Verification Steps

### 1. Start Backend
```bash
cd backend
python run.py

# Should see:
# 🚀 VTO Backend v1.0.0 starting...
# 📝 API Documentation: http://0.0.0.0:8000/docs
# ✅ Server ready!
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Test Backend Health
```bash
curl http://localhost:8000/health

# Expected:
# {"status":"healthy","timestamp":"..."}
```

### 3. Test Try-On Endpoint
```bash
# Test if endpoint exists
curl -X POST http://localhost:8000/api/v1/tryon/process

# Should NOT get "404 Not Found"
# Should get either:
# - 422 Unprocessable Entity (missing files - good!)
# - 501 Not Implemented (endpoint exists but not ready)
```

### 4. Test from Frontend
Open browser console and run:
```javascript
// Test connection
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log('✓ Backend connected:', d))
  .catch(e => console.error('✗ Connection failed:', e))

// Test CORS
fetch('http://localhost:8000/api/v1/tryon/process', {
  method: 'POST'
})
  .then(r => console.log('✓ CORS OK, Status:', r.status))
  .catch(e => console.error('✗ CORS blocked:', e))
```

---

## 🐛 Common Issues & Solutions

### Issue: "Failed to fetch"
**Cause:** Backend not running or wrong URL  
**Fix:** 
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it
python run.py
```

### Issue: "CORS policy blocked"
**Cause:** Frontend origin not in ALLOWED_ORIGINS  
**Fix:** Update `app/core/config.py`:
```python
ALLOWED_ORIGINS: str = "*"  # Development only
```

### Issue: "404 Not Found"
**Cause:** Endpoint path mismatch  
**Fix:** Either:
- Change frontend to `/api/v1/tryon/try-on`
- Add `/process` endpoint to backend

### Issue: "501 Not Implemented"
**Cause:** Endpoint exists but not implemented  
**Fix:** Implement the endpoint (see Fix 3)

### Issue: "422 Unprocessable Entity"
**Cause:** Missing required fields (user_image, cloth_image)  
**Fix:** This is actually good! Endpoint is working, just needs proper FormData

---

## 🎯 Recommended Solution

**Apply these changes in order:**

### 1. Update Backend Endpoint (5 minutes)

**File:** `app/api/v1/endpoints/tryon.py`

Replace the entire file with the implementation from Fix 3 above.

### 2. Update CORS (1 minute)

**File:** `app/core/config.py` (Line 27)

```python
ALLOWED_ORIGINS: str = "*"  # Allow all origins for development
```

### 3. Restart Backend

```bash
# Stop current server (Ctrl+C)
# Start again
python run.py
```

### 4. Test

Open frontend and click "Try On". Should now work!

---

## 📊 Expected Results

### Before Fix:
```
Frontend → http://localhost:8000/api/v1/tryon/process
Backend → 404 Not Found
Error: "Cannot connect to server"
```

### After Fix:
```
Frontend → http://localhost:8000/api/v1/tryon/process
Backend → 200 OK with result image
Success: Result displayed
```

---

## 🔍 Debug Checklist

```bash
# 1. Backend running?
curl http://localhost:8000/health
# ✓ Should return {"status":"healthy"}

# 2. Endpoint exists?
curl -X POST http://localhost:8000/api/v1/tryon/process
# ✓ Should NOT return 404

# 3. CORS configured?
# Check browser console for CORS errors
# ✓ Should not see "CORS policy" errors

# 4. FormData correct?
# Check browser Network tab
# ✓ Should see user_image and cloth_image in request

# 5. Response received?
# Check browser Network tab
# ✓ Should see 200 OK with JSON response
```

---

## 💡 Quick Test Script

Create `test_connection.py`:

```python
import requests

# Test 1: Health check
try:
    r = requests.get('http://localhost:8000/health')
    print(f"✓ Health check: {r.status_code} - {r.json()}")
except Exception as e:
    print(f"✗ Health check failed: {e}")

# Test 2: Try-on endpoint exists
try:
    r = requests.post('http://localhost:8000/api/v1/tryon/process')
    print(f"✓ Try-on endpoint: {r.status_code}")
    if r.status_code == 404:
        print("  ✗ Endpoint not found!")
    elif r.status_code == 422:
        print("  ✓ Endpoint exists (missing files)")
    elif r.status_code == 501:
        print("  ⚠ Endpoint exists but not implemented")
except Exception as e:
    print(f"✗ Try-on endpoint failed: {e}")

# Test 3: CORS
try:
    r = requests.options('http://localhost:8000/api/v1/tryon/process')
    print(f"✓ CORS preflight: {r.status_code}")
    print(f"  Allow-Origin: {r.headers.get('Access-Control-Allow-Origin', 'Not set')}")
except Exception as e:
    print(f"✗ CORS check failed: {e}")
```

Run:
```bash
python test_connection.py
```

---

## ✅ Summary

**Main Issue:** Frontend calling `/api/v1/tryon/process` but backend only has `/api/v1/tryon/try-on`

**Solution:** Add `/process` endpoint to backend (recommended) OR change frontend URL

**Apply Fix 3 to implement the endpoint and your connection will work!**

