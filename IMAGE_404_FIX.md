# Image 404 Error - Complete Fix Guide

## 🔴 Problem Identified

**Error:** Browser console shows 404 errors for clothing images
```
Failed to load resource: 404 (Not Found)
assets/clothes/shirt1.png
assets/clothes/pants1.png
```

**Root Cause:** Image files don't exist in the `frontend/assets/clothes/` directory

---

## 🔍 Diagnosis

### Current State
```
frontend/
├── index.html
├── script.js
├── style.css
└── assets/
    └── clothes/
        └── clothes.json  ✅ EXISTS
        └── shirt1.png    ❌ MISSING
        └── shirt2.png    ❌ MISSING
        └── pants1.png    ❌ MISSING
        └── (etc.)        ❌ MISSING
```

### What's Configured
`clothes.json` references 6 images:
- shirt1.png
- shirt2.png
- shirt3.png
- pants1.png
- pants2.png
- dress1.png

### What's Missing
All actual image files are missing!

---

## ✅ Solution Options

### Option 1: Add Real Clothing Images (Recommended)

**Step 1:** Get clothing images
- Download from free stock photo sites (Unsplash, Pexels, Pixabay)
- Use your own clothing photos
- Use AI-generated clothing images

**Step 2:** Prepare images
- Recommended size: 512x512 or 1024x1024 pixels
- Format: PNG (with transparency) or JPG
- Background: Transparent or white
- File names: Match those in `clothes.json`

**Step 3:** Add to project
```bash
# Place images in this folder:
frontend/assets/clothes/
├── shirt1.png
├── shirt2.png
├── shirt3.png
├── pants1.png
├── pants2.png
└── dress1.png
```

---

### Option 2: Use Placeholder Images (Quick Fix)

Create colored placeholder images using Python:

**Create this script:** `create_placeholder_images.py`

```python
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure directory exists
os.makedirs('frontend/assets/clothes', exist_ok=True)

# Define placeholder images
placeholders = [
    ('shirt1.png', 'Blue Shirt', (100, 150, 200)),
    ('shirt2.png', 'White Shirt', (240, 240, 240)),
    ('shirt3.png', 'Red T-Shirt', (200, 100, 100)),
    ('pants1.png', 'Blue Jeans', (80, 120, 180)),
    ('pants2.png', 'Black Pants', (50, 50, 50)),
    ('dress1.png', 'Summer Dress', (255, 200, 150)),
]

for filename, text, color in placeholders:
    # Create 512x512 image
    img = Image.new('RGB', (512, 512), color=color)
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((512 - text_width) // 2, (512 - text_height) // 2)
    
    draw.text(position, text, fill='white', font=font)
    
    # Save
    filepath = f'frontend/assets/clothes/{filename}'
    img.save(filepath)
    print(f'✓ Created {filepath}')

print('\n✅ All placeholder images created!')
```

**Run it:**
```bash
python create_placeholder_images.py
```

---

### Option 3: Use Online Placeholder Service

Update `script.js` to use placeholder.com:

**Find this in `script.js` (around line 352):**
```javascript
const imagePath = CONFIG.clothesBasePath + cloth.image;
item.innerHTML = `
    <img src="${imagePath}" alt="${cloth.name}" class="cloth-image" loading="lazy">
    <div class="cloth-label">${cloth.name}</div>
`;
```

**Replace with:**
```javascript
// Use placeholder if image doesn't exist
const imagePath = CONFIG.clothesBasePath + cloth.image;
const placeholderUrl = `https://via.placeholder.com/512x512/4A90E2/FFFFFF?text=${encodeURIComponent(cloth.name)}`;

item.innerHTML = `
    <img src="${imagePath}" 
         alt="${cloth.name}" 
         class="cloth-image" 
         loading="lazy"
         onerror="this.src='${placeholderUrl}'">
    <div class="cloth-label">${cloth.name}</div>
`;
```

This will show a placeholder if the real image fails to load.

---

### Option 4: Disable Image Loading (Temporary)

If you just want to test other features, modify `clothes.json` to mark all items as placeholders:

**Update `clothes.json`:**
```json
{
  "clothes": [
    {
      "id": "shirt1",
      "name": "Blue Casual Shirt",
      "category": "shirt",
      "placeholder": true
    },
    {
      "id": "shirt2",
      "name": "White Formal Shirt",
      "category": "shirt",
      "placeholder": true
    }
  ]
}
```

The frontend already handles placeholder items (shows colored boxes with text).

---

## 🔧 Additional Checks

### Check 1: Verify File Paths

**If images exist but still 404:**

1. **Check case sensitivity:**
   - Windows: Not case-sensitive
   - Linux/Mac: Case-sensitive
   - `Shirt1.png` ≠ `shirt1.png`

2. **Check file extensions:**
   - Ensure `.png` not `.PNG`
   - Ensure no hidden extensions (`.png.jpg`)

3. **Check relative paths:**
   - `index.html` location matters
   - Path is relative to HTML file

### Check 2: Browser DevTools

**Open browser console (F12) and check:**

1. **Network tab:**
   - See exact URL being requested
   - Check if path is correct
   - Look for typos

2. **Console tab:**
   - See 404 errors
   - Check error messages

3. **Test in console:**
   ```javascript
   fetch('assets/clothes/shirt1.png')
     .then(r => console.log('Found!', r.status))
     .catch(e => console.log('Not found!', e))
   ```

### Check 3: Server Configuration

**If using a local server:**

1. **Python HTTP Server:**
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Open: http://localhost:8080

2. **VS Code Live Server:**
   - Right-click `index.html`
   - Select "Open with Live Server"

3. **Node.js http-server:**
   ```bash
   npm install -g http-server
   cd frontend
   http-server -p 8080
   ```

**If opening file directly (file://):**
- Some browsers block local file access
- Use a local server instead

### Check 4: FastAPI Static Files

**If serving frontend through FastAPI:**

Your `app/main.py` should have:
```python
from fastapi.staticfiles import StaticFiles

# Mount frontend directory
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

**Or serve assets separately:**
```python
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
```

---

## 📋 Step-by-Step Debugging Checklist

### Step 1: Verify Directory Structure
```bash
# Check if images exist
ls frontend/assets/clothes/

# Should show:
# clothes.json
# shirt1.png
# shirt2.png
# pants1.png
# etc.
```

### Step 2: Check File Names
```bash
# List all files with details
ls -la frontend/assets/clothes/

# Verify:
# - Correct names (case-sensitive)
# - Correct extensions (.png not .PNG)
# - No spaces in names
```

### Step 3: Test Image Access
```bash
# If using Python server
cd frontend
python -m http.server 8080

# Open browser to:
# http://localhost:8080/assets/clothes/shirt1.png
# Should show the image
```

### Step 4: Check Browser Console
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Look for failed requests
5. Click on failed request to see details

### Step 5: Verify JSON Configuration
```bash
# Check clothes.json
cat frontend/assets/clothes/clothes.json

# Verify image names match actual files
```

### Step 6: Test with Placeholder
```javascript
// In browser console
document.querySelector('.cloth-image').src = 'https://via.placeholder.com/512'
// If this works, path issue confirmed
```

---

## 🚀 Quick Fix (Choose One)

### Quick Fix A: Create Placeholder Images (2 minutes)
```bash
python create_placeholder_images.py
```

### Quick Fix B: Use Online Placeholders (1 minute)
Add `onerror` handler to images in `script.js` (see Option 3 above)

### Quick Fix C: Mark as Placeholders (30 seconds)
Add `"placeholder": true` to all items in `clothes.json`

### Quick Fix D: Download Sample Images (5 minutes)
1. Go to https://unsplash.com/s/photos/clothing
2. Download 6 clothing images
3. Rename to match `clothes.json`
4. Place in `frontend/assets/clothes/`

---

## ✅ Verification

After applying fix, verify:

1. **No 404 errors in console:**
   ```
   ✓ No "Failed to load resource" errors
   ```

2. **Images visible in UI:**
   ```
   ✓ Clothing grid shows images
   ✓ No broken image icons
   ```

3. **Can select clothing:**
   ```
   ✓ Click on clothing item
   ✓ Item gets selected (highlighted)
   ✓ No errors in console
   ```

4. **Test image loading:**
   ```javascript
   // In browser console
   fetch('assets/clothes/shirt1.png')
     .then(r => console.log('✓ Image found:', r.status))
   ```

---

## 🎯 Recommended Solution

**For Development/Testing:**
Use **Option 2** (Placeholder Images) - Quick and works offline

**For Production:**
Use **Option 1** (Real Images) - Professional appearance

**For Quick Demo:**
Use **Option 3** (Online Placeholders) - No setup needed

---

## 📝 Summary

**Problem:** Images referenced in `clothes.json` don't exist in filesystem

**Cause:** Only JSON file exists, no actual image files

**Solution:** Add images using one of 4 options:
1. Real clothing images (best)
2. Generated placeholders (quick)
3. Online placeholders (easiest)
4. Disable images (temporary)

**Next Steps:**
1. Choose a solution above
2. Apply the fix
3. Refresh browser
4. Verify no 404 errors
5. Test clothing selection

---

## 🆘 Still Not Working?

If images still don't load after trying above:

1. **Share exact error message** from console
2. **Share file structure** output of `ls -R frontend/assets/`
3. **Share how you're running** (file://, local server, FastAPI)
4. **Share browser** (Chrome, Firefox, Safari)

Common issues:
- Wrong working directory
- CORS blocking local files
- Typo in file names
- Wrong file permissions
- Cache not cleared

**Clear browser cache:**
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete
- Or hard refresh: Ctrl+F5
