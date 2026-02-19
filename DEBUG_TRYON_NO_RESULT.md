# Debug: Try-On Shows Processing But No Result

## Problem
After clicking "Try On", button shows "Processing..." but no result is displayed.

## Diagnostic Steps

### Step 1: Check Browser Console
1. Press `F12` to open Developer Tools
2. Go to "Console" tab
3. Click "Try On" button
4. Look for:
   - ✓ "Try-on request started"
   - ✓ "Loading result image from: ..."
   - ✓ "Result displayed: ..."
   - ❌ Any red error messages

### Step 2: Check Network Tab
1. Press `F12` → "Network" tab
2. Click "Try On" button
3. Look for request to `/api/v1/tryon/process`
4. Check:
   - Status: Should be `200 OK`
   - Response: Should contain `image_url` or `url`
   - Time: How long it took

### Step 3: Check Backend Logs
Look at your terminal where backend is running. You should see:
```
🚀 TRYON REQUEST STARTED
📥 STEP 1: Reading images...
✓ User image loaded: ...
✓ Cloth image loaded: ...
...
✅ TRYON REQUEST COMPLETED SUCCESSFULLY
```

If it stops at any step, that's where the issue is.

## Common Issues

### Issue 1: Backend Hangs During Processing
**Symptoms:**
- Button stays on "Processing..." forever
- No response from backend
- Backend logs stop at "STEP 6: Warping cloth"

**Cause:** TPS warping is computationally intensive

**Fix:** Already applied in `app/api/v1/endpoints/tryon.py` (vectorized TPS)

**Verify Fix:**
```python
# Check if vectorized TPS is being used
# In app/services/ml/cloth_warping.py, _apply_tps() should use:
# np.sum(..., axis=1) instead of nested loops
```

### Issue 2: Result URL Not Returned
**Symptoms:**
- Backend completes successfully
- Console shows: "No image URL in response"
- Network tab shows 200 OK but no `image_url` in response

**Check Backend Response:**
```javascript
// In browser console after try-on:
// Look for the response object
// Should contain: { status: 'success', image_url: '...', url: '...' }
```

**Fix:** Backend should return both `image_url` and `url` fields

### Issue 3: CORS Error
**Symptoms:**
- Console shows: "CORS policy: No 'Access-Control-Allow-Origin' header"
- Network tab shows request failed

**Fix:** Already applied in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 4: Image File Not Saved
**Symptoms:**
- Backend completes
- Response contains URL
- But image fails to load (404)

**Check:**
```bash
# Check if results directory exists and has files
ls -la results/
```

**Fix:** Ensure `results/` directory exists and backend has write permissions

### Issue 5: Static Files Not Served
**Symptoms:**
- Image saved successfully
- URL looks correct: `/results/tryon_result_xxx.jpg`
- But browser gets 404 when loading image

**Check:** `app/main.py` should have:
```python
from fastapi.staticfiles import StaticFiles
app.mount("/results", StaticFiles(directory="results"), name="results")
```

### Issue 6: Result Section Not Showing
**Symptoms:**
- Image loads successfully
- Console shows: "Result displayed: ..."
- But result section is not visible on page

**Check:**
```javascript
// In browser console:
const resultSection = document.getElementById('resultSection');
console.log('Result section:', {
    exists: !!resultSection,
    display: resultSection?.style.display,
    visible: resultSection?.offsetHeight > 0
});
```

**Fix:** Result section should have `display: block` after processing

## Diagnostic Script

Run this in browser console (F12) to diagnose:

```javascript
// Diagnostic script for try-on result issue
console.log('=== TRY-ON DIAGNOSTIC ===');

// Check DOM elements
const elements = {
    resultSection: document.getElementById('resultSection'),
    resultCanvas: document.getElementById('resultCanvas'),
    resultImage: document.getElementById('resultImage'),
    tryonBtn: document.getElementById('tryonBtn')
};

console.log('1. DOM Elements:', {
    resultSection: !!elements.resultSection,
    resultCanvas: !!elements.resultCanvas,
    resultImage: !!elements.resultImage,
    tryonBtn: !!elements.tryonBtn
});

// Check result section visibility
if (elements.resultSection) {
    console.log('2. Result Section:', {
        display: elements.resultSection.style.display,
        offsetHeight: elements.resultSection.offsetHeight,
        visible: elements.resultSection.offsetHeight > 0
    });
}

// Check canvas
if (elements.resultCanvas) {
    console.log('3. Result Canvas:', {
        display: elements.resultCanvas.style.display,
        width: elements.resultCanvas.width,
        height: elements.resultCanvas.height
    });
}

// Check state
if (typeof state !== 'undefined') {
    console.log('4. Application State:', {
        userImage: !!state.userImage,
        clothImage: !!state.clothImage,
        selectedCloth: !!state.selectedCloth,
        resultImageUrl: state.resultImageUrl,
        resultImage: !!state.resultImage
    });
}

// Test backend connection
console.log('5. Testing backend connection...');
fetch('http://localhost:8000/api/v1/tryon/process', {
    method: 'OPTIONS'
})
.then(response => {
    console.log('Backend connection:', response.ok ? '✓ OK' : '✗ Failed');
})
.catch(error => {
    console.error('Backend connection: ✗ Failed', error.message);
});

console.log('=== END DIAGNOSTIC ===');
```

## Step-by-Step Debug Process

### 1. Verify Backend is Running
```bash
# Should show: INFO:     Uvicorn running on http://127.0.0.1:8000
# If not running, start it:
uvicorn app.main:app --reload
```

### 2. Test Backend Endpoint Manually
```bash
# Create test images
curl -X POST http://localhost:8000/api/v1/tryon/process \
  -F "user_image=@test_person.jpg" \
  -F "cloth_image=@test_cloth.jpg"
```

Expected response:
```json
{
  "status": "success",
  "file_id": "tryon_result_xxx",
  "image_url": "/results/tryon_result_xxx.jpg",
  "url": "/results/tryon_result_xxx.jpg",
  "message": "Try-on completed successfully",
  "time_taken": 2.5
}
```

### 3. Check Frontend Request
Open browser console and monitor the try-on request:
```javascript
// This should be logged when you click Try On:
console.log('Try-on request started');
console.log('FormData:', formData);
console.log('Sending to:', 'http://localhost:8000/api/v1/tryon/process');
```

### 4. Check Response Handling
```javascript
// After backend responds, this should be logged:
console.log('Try-on response:', result);
console.log('Loading result image from:', imageUrl);
```

### 5. Check Image Loading
```javascript
// When image loads, this should be logged:
console.log('Result displayed:', {
    width: img.width,
    height: img.height,
    url: imageUrl
});
```

## Quick Fixes

### Fix 1: Force Show Result Section
```javascript
// Run in console to force show result section:
const resultSection = document.getElementById('resultSection');
if (resultSection) {
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
    console.log('Result section forced visible');
}
```

### Fix 2: Manually Load Result Image
```javascript
// If you know the result URL, load it manually:
const imageUrl = 'http://localhost:8000/results/tryon_result_xxx.jpg';
const resultImage = document.getElementById('resultImage');
resultImage.src = imageUrl;
resultImage.style.display = 'block';
document.getElementById('resultSection').style.display = 'block';
```

### Fix 3: Check Results Directory
```bash
# Create results directory if missing:
mkdir -p results
chmod 755 results

# Check if files are being created:
ls -lah results/
```

### Fix 4: Add Debug Logging to Frontend
Add this to `frontend/script.js` in the `displayResult` function:

```javascript
async function displayResult(result, timeTaken) {
    console.log('=== DISPLAY RESULT CALLED ===');
    console.log('Result object:', result);
    console.log('Time taken:', timeTaken);
    
    try {
        // Show result section
        console.log('Showing result section...');
        elements.resultSection.style.display = 'block';
        console.log('Result section display:', elements.resultSection.style.display);
        
        // ... rest of function
    } catch (error) {
        console.error('=== DISPLAY RESULT ERROR ===', error);
        throw error;
    }
}
```

## Expected Flow

1. User clicks "Try On"
2. Button shows "Processing..."
3. Frontend sends FormData to backend
4. Backend processes (2-5 seconds)
5. Backend returns JSON with `image_url`
6. Frontend receives response
7. Frontend calls `displayResult()`
8. Result section becomes visible
9. Image loads and displays
10. Button returns to "Try On"

## If Still Not Working

Run the complete diagnostic and share:
1. Browser console output
2. Backend terminal output
3. Network tab screenshot
4. Result of diagnostic script

This will help identify the exact point of failure.
