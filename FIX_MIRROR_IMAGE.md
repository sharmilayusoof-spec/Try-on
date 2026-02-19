# Fix: Camera Mirror Image Issue

## 🔴 Problem

When capturing photos from the front-facing camera:
1. Image appears as mirror/flipped horizontally
2. Pose detection fails because the person appears reversed
3. Try-on doesn't work with camera-captured images

## 🎯 Root Cause

Front-facing cameras show a mirrored view (like looking in a mirror), but when you capture the image, it needs to be flipped horizontally to show the correct orientation for pose detection.

**Current code:**
```javascript
ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

This draws the video frame as-is (mirrored).

## ✅ Solution

Flip the image horizontally before capturing by using canvas transform.

### Fix 1: Update `capturePhoto()` function

**File:** `frontend/script.js` (around line 762)

**Find:**
```javascript
async function capturePhoto() {
    if (!state.cameraStream) {
        showStatus('Camera not active', 'error');
        return;
    }
    
    try {
        showStatus('Capturing photo...', 'info');
        
        // Get video dimensions
        const video = elements.cameraVideo;
        const canvas = elements.cameraCanvas;
        
        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw current frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

**Replace with:**
```javascript
async function capturePhoto() {
    if (!state.cameraStream) {
        showStatus('Camera not active', 'error');
        return;
    }
    
    try {
        showStatus('Capturing photo...', 'info');
        
        // Get video dimensions
        const video = elements.cameraVideo;
        const canvas = elements.cameraCanvas;
        
        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw current frame to canvas (FLIPPED HORIZONTALLY)
        const ctx = canvas.getContext('2d');
        
        // Flip horizontally
        ctx.save();
        ctx.scale(-1, 1);
        ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
        ctx.restore();
```

### Fix 2: Update `captureRealtimeFrame()` function

**File:** `frontend/script.js` (around line 1010)

**Find:**
```javascript
async function captureRealtimeFrame() {
    try {
        const video = elements.cameraVideo;
        const canvas = elements.cameraCanvas;
        
        // Set canvas size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw frame
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

**Replace with:**
```javascript
async function captureRealtimeFrame() {
    try {
        const video = elements.cameraVideo;
        const canvas = elements.cameraCanvas;
        
        // Set canvas size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw frame (FLIPPED HORIZONTALLY)
        const ctx = canvas.getContext('2d');
        
        // Flip horizontally
        ctx.save();
        ctx.scale(-1, 1);
        ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
        ctx.restore();
```

### Fix 3: Keep Video Preview Mirrored (Optional)

Users expect to see themselves mirrored in the camera preview (like a mirror), but the captured image should be flipped.

**File:** `frontend/style.css`

**Add this CSS:**
```css
#cameraVideo {
    transform: scaleX(-1);
    -webkit-transform: scaleX(-1);
}
```

This keeps the video preview mirrored (natural for users) but the captured image will be correctly oriented.

## 🔍 How It Works

### Canvas Transform Explanation

```javascript
ctx.save();              // Save current state
ctx.scale(-1, 1);        // Flip horizontally (negative X scale)
ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
                         // Draw at negative X position
ctx.restore();           // Restore original state
```

**What happens:**
1. `scale(-1, 1)` flips the canvas horizontally
2. Drawing at `-canvas.width` compensates for the flip
3. Result: Image is flipped to correct orientation

### Visual Explanation

**Before (Mirrored):**
```
Camera shows: 👤 (person facing left)
Captured:     👤 (still facing left - WRONG for pose detection)
```

**After (Flipped):**
```
Camera shows: 👤 (person facing left - mirrored view)
Captured:     🤴 (person facing right - CORRECT orientation)
```

## 🧪 Testing

### Test 1: Capture Photo
1. Click "Use Camera"
2. Allow camera access
3. Click "Capture Photo"
4. Check uploaded image - should NOT be mirrored
5. Try "Try On" - pose detection should work

### Test 2: Real-time Mode
1. Click "Use Camera"
2. Enable "Real-time Mode"
3. Select clothing
4. Check if pose detection works
5. Result should display correctly

### Test 3: Verify Orientation
```javascript
// In browser console after capturing:
const img = document.getElementById('userImagePreview');
console.log('Image dimensions:', img.naturalWidth, 'x', img.naturalHeight);

// Take a photo with text/writing visible
// After capture, text should be readable (not mirrored)
```

## 📊 Before vs After

### Before Fix
```
Camera Preview: 👤 (mirrored - looks normal)
Captured Image: 👤 (mirrored - WRONG)
Pose Detection: ❌ FAILS (person appears reversed)
Try-On Result:  ❌ FAILS
```

### After Fix
```
Camera Preview: 👤 (mirrored - looks normal)
Captured Image: 🤴 (flipped - CORRECT)
Pose Detection: ✅ WORKS (person in correct orientation)
Try-On Result:  ✅ WORKS
```

## 🎯 Why This Happens

**Front-facing cameras:**
- Show mirrored view (like a mirror)
- This is intentional for user comfort
- But AI models expect non-mirrored images

**Back-facing cameras:**
- Show correct orientation
- No flipping needed

**Solution:**
- Keep preview mirrored (CSS transform on video)
- Flip image when capturing (canvas transform)
- Best of both worlds!

## 🔧 Alternative Solutions

### Solution A: Flip on Backend
```python
# In backend pose detection
import cv2

def flip_if_needed(image):
    # Flip horizontally
    return cv2.flip(image, 1)
```

**Pros:** No frontend changes
**Cons:** All images get flipped (even correct ones)

### Solution B: Detect and Flip
```javascript
// Detect if image is mirrored
function isImageMirrored(landmarks) {
    // Check if left shoulder is on right side
    const leftShoulder = landmarks.find(l => l.name === 'left_shoulder');
    const rightShoulder = landmarks.find(l => l.name === 'right_shoulder');
    return leftShoulder.x > rightShoulder.x;
}
```

**Pros:** Smart detection
**Cons:** Complex, requires pose detection first

### Solution C: User Choice
```html
<label>
    <input type="checkbox" id="flipImage">
    Flip image horizontally
</label>
```

**Pros:** User control
**Cons:** Extra step, confusing for users

**Recommended: Use Solution in this document (flip during capture)**

## 📝 Summary

**Problem:** Camera captures mirrored images → Pose detection fails

**Solution:** Flip image horizontally during capture using canvas transform

**Files to Edit:**
- `frontend/script.js` - Update `capturePhoto()` and `captureRealtimeFrame()`
- `frontend/style.css` - Add video mirror CSS (optional)

**Result:** Camera preview stays mirrored (natural), but captured images are correctly oriented for pose detection

## ✅ Checklist

- [ ] Update `capturePhoto()` function
- [ ] Update `captureRealtimeFrame()` function
- [ ] Add CSS to mirror video preview (optional)
- [ ] Test camera capture
- [ ] Test real-time mode
- [ ] Verify pose detection works
- [ ] Verify try-on works

Apply these fixes and your camera captures will work correctly with pose detection! 🎉
