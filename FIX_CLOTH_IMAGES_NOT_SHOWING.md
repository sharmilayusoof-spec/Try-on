# Fix: Cloth Images Not Showing (Only Names Visible)

## 🔴 Problem

In Step 2, clothing items show only names but no images.

## 🔍 Quick Diagnosis

### Option 1: Use Diagnostic Tool (Recommended)

1. **Open your app** in browser
2. **Press F12** to open DevTools
3. **Go to Console tab**
4. **Copy and paste** the contents of `diagnose_and_fix_images.js`
5. **Press Enter**
6. **Follow the instructions** shown in console

### Option 2: Manual Check

**In browser console, run:**
```javascript
// Check if images exist
document.querySelectorAll('.cloth-image').length
// Should return: 6

// Check image dimensions
document.querySelectorAll('.cloth-image').forEach((img, i) => {
  const rect = img.getBoundingClientRect();
  console.log(`Image ${i}: ${rect.width}x${rect.height}`);
});
// Should show dimensions > 0, not 0x0
```

## ✅ Quick Fix (Apply in Browser Console)

**Run this in browser console:**
```javascript
// Fix all cloth images
document.querySelectorAll('.cloth-image').forEach(img => {
  img.style.display = 'block';
  img.style.flex = '1';
  img.style.width = '100%';
  img.style.height = '100%';
  img.style.objectFit = 'cover';
});

// Fix containers
document.querySelectorAll('.cloth-item').forEach(item => {
  item.style.minHeight = '150px';
});

console.log('✓ Fix applied! Check if images are now visible.');
```

## 🔧 Permanent Fix (Edit CSS File)

**File:** `frontend/style.css`

**Find the `.cloth-item` section (around line 259) and verify it has:**
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
    min-height: 150px;  /* ← MUST HAVE THIS */
    height: auto;       /* ← MUST HAVE THIS */
}
```

**Find the `.cloth-image` section (around line 284) and verify it has:**
```css
.cloth-image {
    width: 100%;
    height: 100%;
    flex: 1;           /* ← MUST HAVE THIS */
    object-fit: cover;
    display: block;    /* ← MUST HAVE THIS */
    transition: transform var(--transition-base);
}
```

**If missing, add this at the END of style.css:**
```css
/* EMERGENCY FIX: Force cloth images to display */
.cloth-item {
    min-height: 150px !important;
    height: auto !important;
}

.cloth-image {
    flex: 1 !important;
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
}
```

## 🧪 Test Image Loading

**Open this test page:**
```
open check_cloth_images.html
```

This will show:
- ✓ Which images load successfully
- ✗ Which images fail to load
- Exact error messages

**If images fail to load:**
```bash
# Create placeholder images
python create_placeholder_images.py

# Verify they were created
ls frontend/assets/clothes/
```

## 📊 Common Causes & Solutions

| Symptom | Cause | Solution |
|---------|-------|----------|
| Only names show | Images have 0x0 size | Add `flex: 1` to `.cloth-image` |
| Blank spaces | Images failed to load | Run `create_placeholder_images.py` |
| Images very small | Container has no height | Add `min-height: 150px` to `.cloth-item` |
| Images cut off | Overflow hidden | Check parent overflow |

## 🎯 Step-by-Step Fix Process

### Step 1: Check if images exist
```bash
ls frontend/assets/clothes/
# Should show: shirt1.png, shirt2.png, pants1.png, etc.
```

**If missing:**
```bash
python create_placeholder_images.py
```

### Step 2: Check browser console
1. Open app in browser
2. Press F12
3. Look for errors
4. Check if you see: "✓ Image loaded: [name]"

**If you see errors:**
- "Failed to load image" → Images don't exist
- No messages → JavaScript not running

### Step 3: Apply CSS fix
1. Open `frontend/style.css`
2. Add the emergency fix CSS (see above)
3. Save file
4. Hard refresh browser (Ctrl+Shift+R)

### Step 4: Verify fix worked
```javascript
// In browser console:
document.querySelectorAll('.cloth-image').forEach((img, i) => {
  const rect = img.getBoundingClientRect();
  console.log(`Image ${i}: ${rect.width}x${rect.height} - ${rect.width > 0 ? '✓ VISIBLE' : '✗ HIDDEN'}`);
});
```

## 🔍 Advanced Debugging

### Check if images are in DOM but hidden

**In browser console:**
```javascript
// Get all cloth items
const items = document.querySelectorAll('.cloth-item');
console.log('Cloth items:', items.length);

// Check each item
items.forEach((item, i) => {
  const img = item.querySelector('.cloth-image');
  const rect = item.getBoundingClientRect();
  
  console.log(`Item ${i}:`, {
    hasImage: !!img,
    itemSize: `${rect.width}x${rect.height}`,
    imgSrc: img?.src,
    imgSize: img ? `${img.naturalWidth}x${img.naturalHeight}` : 'N/A',
    displaySize: img ? `${img.getBoundingClientRect().width}x${img.getBoundingClientRect().height}` : 'N/A'
  });
});
```

### Force images to show

**In browser console:**
```javascript
// Nuclear option - force everything visible
document.querySelectorAll('.cloth-item').forEach(item => {
  item.style.cssText = `
    min-height: 150px !important;
    height: 150px !important;
    display: flex !important;
    flex-direction: column !important;
  `;
});

document.querySelectorAll('.cloth-image').forEach(img => {
  img.style.cssText = `
    flex: 1 !important;
    display: block !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    visibility: visible !important;
    opacity: 1 !important;
  `;
});

console.log('✓ Nuclear fix applied!');
```

## 📝 Checklist

- [ ] Images exist in `frontend/assets/clothes/`
- [ ] Browser console shows "✓ Image loaded" messages
- [ ] No 404 errors in Network tab
- [ ] `.cloth-item` has `min-height: 150px`
- [ ] `.cloth-image` has `flex: 1` and `display: block`
- [ ] Hard refresh browser (Ctrl+Shift+R)
- [ ] Images are now visible

## 🆘 Still Not Working?

1. **Open** `check_cloth_images.html` in browser
2. **Check** which images load/fail
3. **Run** diagnostic script in console
4. **Share** the console output for more help

## ✅ Expected Result

After applying the fix:
- ✅ 6 colored placeholder images visible
- ✅ Each image ~150x150 pixels
- ✅ Image + name displayed for each item
- ✅ Hover effect works
- ✅ Click to select works

Your cloth images should now be visible! 🎉
