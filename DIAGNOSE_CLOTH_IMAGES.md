# Cloth Images Not Showing - Diagnostic Guide

## Current Status
✅ All 6 PNG images exist in `frontend/assets/clothes/`
✅ CSS fixes are present (flex: 1, min-height: 150px)
✅ JavaScript uses `loading="eager"` to avoid lazy loading
✅ Config path is correct: `assets/clothes/`

## Issue
User reports cloth images show only names, not images in Step 2.

## Root Cause Analysis

### Most Likely Causes:
1. **Browser cache** - Old CSS/JS files cached without the fixes
2. **Wrong HTML file** - User might be viewing old `index.html` instead of updated version
3. **CSS not applied** - Styles overridden or not loaded
4. **Image dimensions collapsed** - Despite CSS fixes, images still 0x0

## Diagnostic Steps

### Step 1: Hard Refresh Browser
**CRITICAL: Do this first!**

```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

This clears cached CSS and JavaScript files.

### Step 2: Verify Which HTML File You're Using

Open browser console (F12) and run:
```javascript
console.log(window.location.href);
```

Make sure you're viewing:
- `http://localhost:8000/index.html` (correct)
- NOT `http://localhost:8000/index_clean.html` (different UI)

### Step 3: Check If Images Are Loading

Run in console:
```javascript
// Check if images exist in DOM
const images = document.querySelectorAll('.cloth-image');
console.log(`Found ${images.length} cloth images`);

// Check each image
images.forEach((img, i) => {
    console.log(`Image ${i + 1}:`, {
        src: img.src,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        displayWidth: img.offsetWidth,
        displayHeight: img.offsetHeight,
        computed: window.getComputedStyle(img)
    });
});
```

### Step 4: Check CSS Applied to Images

Run in console:
```javascript
const images = document.querySelectorAll('.cloth-image');
images.forEach((img, i) => {
    const styles = window.getComputedStyle(img);
    console.log(`Image ${i + 1} CSS:`, {
        display: styles.display,
        flex: styles.flex,
        width: styles.width,
        height: styles.height,
        objectFit: styles.objectFit,
        visibility: styles.visibility,
        opacity: styles.opacity
    });
});
```

### Step 5: Check Container CSS

Run in console:
```javascript
const containers = document.querySelectorAll('.cloth-item');
containers.forEach((container, i) => {
    const styles = window.getComputedStyle(container);
    console.log(`Container ${i + 1} CSS:`, {
        display: styles.display,
        flexDirection: styles.flexDirection,
        minHeight: styles.minHeight,
        height: styles.height,
        width: styles.width
    });
});
```

## Quick Fixes

### Fix 1: Force CSS Reload
Add this to browser console:
```javascript
// Force reload CSS
const links = document.querySelectorAll('link[rel="stylesheet"]');
links.forEach(link => {
    const href = link.href.split('?')[0];
    link.href = href + '?v=' + Date.now();
});
```

### Fix 2: Emergency CSS Override
If CSS fixes aren't applied, run this in console:
```javascript
// Add emergency CSS
const style = document.createElement('style');
style.textContent = `
    .cloth-item {
        min-height: 150px !important;
        height: auto !important;
        display: flex !important;
        flex-direction: column !important;
    }
    .cloth-image {
        flex: 1 !important;
        display: block !important;
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
`;
document.head.appendChild(style);
console.log('Emergency CSS applied! Refresh cloth grid.');
```

### Fix 3: Force Re-render Cloth Grid
Run in console:
```javascript
// Force re-render
if (typeof renderClothes === 'function') {
    renderClothes();
    console.log('Cloth grid re-rendered');
} else {
    console.error('renderClothes function not found');
}
```

## Expected Output

### When Working Correctly:
```
Found 6 cloth images
Image 1: {
    src: "http://localhost:8000/assets/clothes/shirt1.png",
    naturalWidth: 512,
    naturalHeight: 512,
    displayWidth: 150,  // Should be > 0
    displayHeight: 150, // Should be > 0
}
```

### When Broken:
```
Found 6 cloth images
Image 1: {
    src: "http://localhost:8000/assets/clothes/shirt1.png",
    naturalWidth: 512,
    naturalHeight: 512,
    displayWidth: 0,    // ❌ Problem!
    displayHeight: 0,   // ❌ Problem!
}
```

## Manual Verification

### Check CSS File Directly
1. Open `frontend/style.css`
2. Search for `.cloth-image`
3. Verify it has:
```css
.cloth-image {
    width: 100%;
    height: 100%;
    flex: 1;           /* Must have this */
    object-fit: cover;
    display: block;    /* Must have this */
    transition: transform var(--transition-base);
}
```

4. Search for `.cloth-item`
5. Verify it has:
```css
.cloth-item {
    aspect-ratio: 1;
    border: 2px solid var(--border-color);
    border-radius: var(--radius-lg);
    cursor: pointer;
    transition: all var(--transition-base);
    overflow: hidden;
    background: var(--bg-color);
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 150px;  /* Must have this */
    height: auto;       /* Must have this */
}
```

## If Still Not Working

### Nuclear Option: Add Inline Styles
Edit `frontend/script.js`, find `createClothItem` function (around line 337), and change:

```javascript
// OLD:
item.innerHTML = `
    <img src="${imagePath}" alt="${cloth.name}" class="cloth-image" loading="eager">
    <div class="cloth-label">${cloth.name}</div>
`;

// NEW (with inline styles):
item.innerHTML = `
    <img src="${imagePath}" 
         alt="${cloth.name}" 
         class="cloth-image" 
         loading="eager"
         style="flex: 1; display: block; width: 100%; height: 100%; object-fit: cover;">
    <div class="cloth-label">${cloth.name}</div>
`;
```

Then hard refresh (Ctrl+Shift+R).

## Report Back

After trying these steps, report:
1. Which step revealed the issue?
2. What were the console output values?
3. Did hard refresh fix it?
4. Which fix worked?

This will help identify the exact root cause.
