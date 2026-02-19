# Images Not Displaying - Complete Debug Guide

## 🔴 Problem Analysis

**Symptoms:**
- Console shows: "Loaded 6 clothing items" ✅
- Console shows: "Rendered 6 cloth items" ✅
- Console shows: "[Intervention] Images loaded lazily and replaced with placeholders" ⚠️
- No error messages ✅
- **But images are NOT visible** ❌

**Root Causes Identified:**

1. **Lazy Loading Intervention** (Primary Issue)
   - Chrome's lazy loading can replace images with placeholders
   - Images below viewport may not load immediately
   - Can cause blank/invisible images

2. **Possible CSS Issues**
   - Images might be rendered but hidden
   - Z-index, opacity, or display issues
   - Overflow or clipping problems

3. **Path/Loading Issues**
   - Images exist but not loading properly
   - CORS or static file serving issues

---

## 🔍 Step-by-Step Debugging Checklist

### ✅ Step 1: Verify Images Exist

**Check files:**
```bash
ls -la frontend/assets/clothes/
```

**Should show:**
```
shirt1.png
shirt2.png
shirt3.png
pants1.png
pants2.png
dress1.png
clothes.json
```

**If missing, run:**
```bash
python create_placeholder_images.py
```

---

### ✅ Step 2: Check Browser DevTools

**Open DevTools (F12) → Network Tab:**

1. Reload page
2. Filter by "Img"
3. Look for clothing images
4. Check status codes:
   - ✅ 200 = Loading successfully
   - ❌ 404 = File not found
   - ❌ 403 = Permission denied

**Check actual requests:**
```
Should see:
GET /assets/clothes/shirt1.png 200 OK
GET /assets/clothes/shirt2.png 200 OK
etc.
```

---

### ✅ Step 3: Inspect DOM Elements

**In DevTools → Elements Tab:**

1. Find `.cloth-grid` element
2. Expand to see `.cloth-item` children
3. Check each `<img>` tag:
   ```html
   <img src="assets/clothes/shirt1.png" 
        alt="Blue Casual Shirt" 
        class="cloth-image" 
        loading="lazy">
   ```

4. **Check computed styles:**
   - Right-click image → Inspect
   - Look at Styles panel
   - Check for:
     - `display: none` ❌
     - `opacity: 0` ❌
     - `visibility: hidden` ❌
     - `width: 0` or `height: 0` ❌

---

### ✅ Step 4: Test Image Loading Manually

**In Console, run:**
```javascript
// Test if images can be loaded
const testImg = new Image();
testImg.onload = () => console.log('✅ Image loads!');
testImg.onerror = () => console.log('❌ Image failed!');
testImg.src = 'assets/clothes/shirt1.png';

// Check if images are in DOM
document.querySelectorAll('.cloth-image').forEach((img, i) => {
  console.log(`Image ${i}:`, {
    src: img.src,
    complete: img.complete,
    naturalWidth: img.naturalWidth,
    naturalHeight: img.naturalHeight,
    visible: img.offsetWidth > 0 && img.offsetHeight > 0
  });
});
```

**Expected output:**
```javascript
Image 0: {
  src: "http://localhost:8000/assets/clothes/shirt1.png",
  complete: true,
  naturalWidth: 512,
  naturalHeight: 512,
  visible: true
}
```

**If `naturalWidth: 0`** → Image not loaded
**If `visible: false`** → CSS hiding issue

---

### ✅ Step 5: Check Lazy Loading Behavior

**The "[Intervention]" message indicates Chrome is:**
- Deferring image loading
- Replacing with placeholders
- Waiting for images to enter viewport

**Test by scrolling:**
1. Scroll down to clothing section
2. Wait 2-3 seconds
3. Check if images appear

**If images appear after scrolling** → Lazy loading issue confirmed

---

### ✅ Step 6: Verify CSS Rendering

**Check computed dimensions:**
```javascript
document.querySelectorAll('.cloth-item').forEach((item, i) => {
  const img = item.querySelector('.cloth-image');
  const computed = window.getComputedStyle(img);
  console.log(`Item ${i}:`, {
    display: computed.display,
    visibility: computed.visibility,
    opacity: computed.opacity,
    width: computed.width,
    height: computed.height,
    zIndex: computed.zIndex
  });
});
```

**Should show:**
```javascript
{
  display: "block",
  visibility: "visible",
  opacity: "1",
  width: "150px",  // or similar
  height: "150px",
  zIndex: "auto"
}
```

---

### ✅ Step 7: Check Static File Serving

**If using FastAPI, verify mount:**

**Check `app/main.py`:**
```python
from fastapi.staticfiles import StaticFiles

# Should have:
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
# OR
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

**Test direct access:**
```
Open in browser:
http://localhost:8000/assets/clothes/shirt1.png
```

Should display the image directly.

---

## ✅ Solutions

### Solution 1: Remove Lazy Loading (Recommended)

**Problem:** `loading="lazy"` causing Chrome intervention

**Fix:** Remove lazy loading attribute

**File:** `frontend/script.js` (around line 354)

**Find:**
```javascript
item.innerHTML = `
    <img src="${imagePath}" alt="${cloth.name}" class="cloth-image" loading="lazy">
    <div class="cloth-label">${cloth.name}</div>
`;
```

**Replace with:**
```javascript
item.innerHTML = `
    <img src="${imagePath}" alt="${cloth.name}" class="cloth-image">
    <div class="cloth-label">${cloth.name}</div>
`;
```

**Or use eager loading:**
```javascript
item.innerHTML = `
    <img src="${imagePath}" alt="${cloth.name}" class="cloth-image" loading="eager">
    <div class="cloth-label">${cloth.name}</div>
`;
```

---

### Solution 2: Force Image Load with JavaScript

**Add after creating image element:**

**File:** `frontend/script.js`

**Find the `createClothItem` function and update:**

```javascript
function createClothItem(cloth) {
    const item = document.createElement('div');
    item.className = 'cloth-item';
    item.dataset.clothId = cloth.id;
    item.dataset.category = cloth.category;
    
    if (cloth.placeholder) {
        // Placeholder item
        item.innerHTML = `
            <div class="cloth-placeholder">
                <p>${cloth.name}</p>
            </div>
        `;
    } else {
        // Real image item
        const imagePath = CONFIG.clothesBasePath + cloth.image;
        
        // Create image element programmatically
        const img = document.createElement('img');
        img.src = imagePath;
        img.alt = cloth.name;
        img.className = 'cloth-image';
        // Remove lazy loading or set to eager
        img.loading = 'eager';
        
        // Force load
        img.decode().then(() => {
            console.log(`✓ Image loaded: ${cloth.name}`);
        }).catch(err => {
            console.error(`✗ Image failed: ${cloth.name}`, err);
        });
        
        const label = document.createElement('div');
        label.className = 'cloth-label';
        label.textContent = cloth.name;
        
        item.appendChild(img);
        item.appendChild(label);
        
        // Handle image load error
        img.onerror = () => {
            console.error(`Failed to load: ${imagePath}`);
            item.innerHTML = `
                <div class="cloth-placeholder">
                    <p>${cloth.name}</p>
                    <small>Image not found</small>
                </div>
            `;
        };
    }
    
    return item;
}
```

---

### Solution 3: Add Intersection Observer (Advanced)

**For better lazy loading control:**

```javascript
// Add after CONFIG definition
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        }
    });
}, {
    rootMargin: '50px' // Load 50px before entering viewport
});

// In createClothItem function:
const img = document.createElement('img');
img.dataset.src = imagePath; // Use data-src instead
img.alt = cloth.name;
img.className = 'cloth-image';

// Observe the image
imageObserver.observe(img);
```

---

### Solution 4: Fix CSS Issues

**Check if images are being clipped or hidden:**

**File:** `frontend/style.css`

**Add explicit visibility rules:**

```css
.cloth-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    /* Ensure images are visible */
    min-width: 100px;
    min-height: 100px;
}

.cloth-item {
    position: relative;
    aspect-ratio: 1;
    border: 2px solid var(--border-color);
    overflow: visible; /* Changed from hidden if needed */
    background: #f5f5f5; /* Show container */
}

/* Debug: Add background to see container */
.cloth-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    background: #e0e0e0; /* Temporary debug color */
    padding: 1rem;
}
```

---

### Solution 5: Preload Images

**Add to HTML `<head>`:**

```html
<link rel="preload" as="image" href="assets/clothes/shirt1.png">
<link rel="preload" as="image" href="assets/clothes/shirt2.png">
<link rel="preload" as="image" href="assets/clothes/shirt3.png">
<link rel="preload" as="image" href="assets/clothes/pants1.png">
<link rel="preload" as="image" href="assets/clothes/pants2.png">
<link rel="preload" as="image" href="assets/clothes/dress1.png">
```

---

### Solution 6: Add Loading Indicator

**Show loading state while images load:**

```javascript
function createClothItem(cloth) {
    const item = document.createElement('div');
    item.className = 'cloth-item';
    item.dataset.clothId = cloth.id;
    item.dataset.category = cloth.category;
    
    if (!cloth.placeholder) {
        const imagePath = CONFIG.clothesBasePath + cloth.image;
        
        // Add loading state
        item.innerHTML = `
            <div class="image-loading">Loading...</div>
            <img src="${imagePath}" 
                 alt="${cloth.name}" 
                 class="cloth-image" 
                 style="display: none;">
            <div class="cloth-label">${cloth.name}</div>
        `;
        
        const img = item.querySelector('.cloth-image');
        const loader = item.querySelector('.image-loading');
        
        img.onload = () => {
            loader.style.display = 'none';
            img.style.display = 'block';
            console.log(`✓ Loaded: ${cloth.name}`);
        };
        
        img.onerror = () => {
            loader.textContent = 'Failed to load';
            console.error(`✗ Failed: ${cloth.name}`);
        };
    }
    
    return item;
}
```

**Add CSS:**
```css
.image-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background: #f0f0f0;
    color: #666;
    font-size: 14px;
}
```

---

## 🚀 Quick Fix (Apply Now)

### Minimal Fix - Remove Lazy Loading

**1. Open `frontend/script.js`**

**2. Find line ~354:**
```javascript
<img src="${imagePath}" alt="${cloth.name}" class="cloth-image" loading="lazy">
```

**3. Change to:**
```javascript
<img src="${imagePath}" alt="${cloth.name}" class="cloth-image">
```

**4. Save and hard refresh browser (Ctrl+Shift+R)**

**5. Check if images appear**

---

## 🧪 Verification Tests

### Test 1: Visual Check
```
✓ Open frontend/index.html
✓ Scroll to clothing section
✓ Should see 6 colored images
✓ No blank spaces
```

### Test 2: Console Check
```javascript
// Run in browser console
document.querySelectorAll('.cloth-image').forEach((img, i) => {
  console.log(`Image ${i}: ${img.complete ? '✓ Loaded' : '✗ Not loaded'} - ${img.naturalWidth}x${img.naturalHeight}`);
});

// Should show:
// Image 0: ✓ Loaded - 512x512
// Image 1: ✓ Loaded - 512x512
// etc.
```

### Test 3: Network Check
```
✓ Open DevTools → Network tab
✓ Filter by "Img"
✓ Reload page
✓ Should see 6 image requests with status 200
```

### Test 4: Interaction Check
```
✓ Click on any clothing item
✓ Should highlight/select
✓ Image should remain visible
```

---

## 📊 Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Lazy loading | Images blank, appear after scroll | Remove `loading="lazy"` |
| 404 errors | Network shows 404 | Run `create_placeholder_images.py` |
| CSS hidden | Images in DOM but invisible | Check CSS display/opacity |
| CORS error | Console shows CORS error | Fix FastAPI static mount |
| Wrong path | Images load wrong URL | Check `CONFIG.clothesBasePath` |
| Cache issue | Old version showing | Hard refresh (Ctrl+Shift+R) |

---

## 🎯 Expected Result

**After fix, you should see:**

1. **Console:**
   ```
   ✓ Loaded 6 clothing items
   ✓ Rendered 6 cloth items
   ✓ Image loaded: Blue Casual Shirt
   ✓ Image loaded: White Formal Shirt
   (etc.)
   ```

2. **UI:**
   - 6 colored placeholder images visible
   - Each with text label
   - Clickable and selectable
   - No blank spaces

3. **Network:**
   - 6 image requests
   - All status 200 OK
   - No 404 errors

---

## 🆘 Still Not Working?

### Debug Script

Create `debug_images.html` in frontend folder:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Image Debug</title>
    <style>
        .test-image {
            width: 200px;
            height: 200px;
            border: 2px solid red;
            margin: 10px;
        }
    </style>
</head>
<body>
    <h1>Image Loading Test</h1>
    
    <h2>Test 1: Direct Image</h2>
    <img src="assets/clothes/shirt1.png" class="test-image">
    
    <h2>Test 2: With Loading Eager</h2>
    <img src="assets/clothes/shirt2.png" class="test-image" loading="eager">
    
    <h2>Test 3: With Loading Lazy</h2>
    <img src="assets/clothes/shirt3.png" class="test-image" loading="lazy">
    
    <h2>Test 4: JavaScript Created</h2>
    <div id="js-test"></div>
    
    <script>
        const img = document.createElement('img');
        img.src = 'assets/clothes/pants1.png';
        img.className = 'test-image';
        img.onload = () => console.log('✓ JS image loaded');
        img.onerror = () => console.log('✗ JS image failed');
        document.getElementById('js-test').appendChild(img);
        
        // Log all image states
        setTimeout(() => {
            document.querySelectorAll('.test-image').forEach((img, i) => {
                console.log(`Test ${i+1}:`, {
                    src: img.src,
                    complete: img.complete,
                    width: img.naturalWidth,
                    height: img.naturalHeight
                });
            });
        }, 2000);
    </script>
</body>
</html>
```

**Open this file and check which test works.**

---

## 📝 Summary

**Primary Issue:** `loading="lazy"` attribute causing Chrome intervention

**Quick Fix:** Remove `loading="lazy"` from image tags

**File to Edit:** `frontend/script.js` line ~354

**Verification:** Images should appear immediately after refresh

**If still not working:** Run debug checklist above and share results
