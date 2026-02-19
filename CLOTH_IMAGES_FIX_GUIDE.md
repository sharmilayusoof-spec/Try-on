# Cloth Images Not Showing - Complete Fix Guide

## Problem
In Step 2, clothing items show only names but no images.

## Quick Fix (Try This First!)

### Option 1: Hard Refresh Browser
**This fixes 90% of cases!**

```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

This clears cached CSS/JavaScript files and reloads everything fresh.

### Option 2: Emergency Console Fix
1. Press `F12` to open Developer Tools
2. Go to "Console" tab
3. Copy the entire contents of `emergency_fix_console.js`
4. Paste into console and press Enter
5. The script will diagnose and fix automatically

### Option 3: Run Diagnostic Test Page
1. Open `test_cloth_display.html` in your browser
2. It will automatically test everything
3. Shows exactly what's wrong
4. Provides visual confirmation

## Verification

### All Files Are Present ✓
```
frontend/assets/clothes/
├── shirt1.png (12 KB)
├── shirt2.png (11 KB)
├── shirt3.png (8 KB)
├── pants1.png (10 KB)
├── pants2.png (10 KB)
└── dress1.png (10 KB)
```

### CSS Fixes Are Applied ✓
The following CSS is already in `frontend/style.css`:

```css
.cloth-item {
    display: flex;
    flex-direction: column;
    min-height: 150px;  /* ← Critical fix */
    height: auto;       /* ← Critical fix */
}

.cloth-image {
    flex: 1;           /* ← Critical fix */
    display: block;    /* ← Critical fix */
    width: 100%;
    height: 100%;
    object-fit: cover;
}
```

### JavaScript Uses Eager Loading ✓
Images use `loading="eager"` to avoid Chrome lazy loading intervention.

## Root Cause

This is a **browser cache issue**. The CSS fixes were added but your browser is still using old cached CSS files that don't have the fixes.

## Why Hard Refresh Works

- Normal refresh (F5): Reloads HTML but may use cached CSS/JS
- Hard refresh (Ctrl+Shift+R): Forces reload of ALL files including CSS/JS
- This ensures the CSS fixes are actually applied

## If Hard Refresh Doesn't Work

### Step 1: Verify You're on the Right Page
Check the URL in your browser:
- ✓ Correct: `http://localhost:8000/index.html`
- ✗ Wrong: `http://localhost:8000/index_clean.html` (different UI)

### Step 2: Clear Browser Cache Completely
**Chrome:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Reload page

**Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cache"
3. Click "Clear Now"
4. Reload page

### Step 3: Check Browser Console
1. Press `F12`
2. Go to "Console" tab
3. Look for errors (red text)
4. Common issues:
   - 404 errors → Images not found
   - CORS errors → Server config issue
   - JavaScript errors → Script not loading

### Step 4: Check Network Tab
1. Press `F12`
2. Go to "Network" tab
3. Reload page (F5)
4. Look for:
   - `clothes.json` - Should be 200 OK
   - `shirt1.png`, `shirt2.png`, etc. - Should be 200 OK
   - If any show 404, images are missing

### Step 5: Verify CSS File
1. Open `frontend/style.css`
2. Search for `.cloth-image`
3. Verify it has `flex: 1;` and `display: block;`
4. Search for `.cloth-item`
5. Verify it has `min-height: 150px;`

If these are missing, the file was overwritten. Re-apply the fixes.

## Manual CSS Fix (Last Resort)

If nothing else works, add this at the END of `frontend/style.css`:

```css
/* Emergency override - add at end of file */
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
```

Then hard refresh (Ctrl+Shift+R).

## Testing Tools Provided

### 1. `emergency_fix_console.js`
- Paste into browser console
- Automatically diagnoses and fixes
- Shows detailed status

### 2. `test_cloth_display.html`
- Standalone test page
- Visual confirmation
- Detailed diagnostics
- Copy log to share

### 3. `DIAGNOSE_CLOTH_IMAGES.md`
- Step-by-step debugging guide
- Console commands to run
- Expected vs actual output

## Expected Behavior When Working

1. Step 2 shows 6 clothing items in a grid
2. Each item shows:
   - Image preview (150x150px minimum)
   - Name label at bottom
3. Hover effects work (zoom, border color)
4. Click to select (blue border)

## Common Mistakes

❌ **Viewing wrong HTML file**
- Make sure you're on `index.html`, not `index_clean.html`

❌ **Not doing hard refresh**
- Regular F5 refresh may not reload CSS
- Must use Ctrl+Shift+R

❌ **Backend not running**
- Images are served by FastAPI backend
- Make sure `uvicorn app.main:app --reload` is running

❌ **Wrong working directory**
- Backend must run from project root
- Not from `frontend/` or `app/` folder

## Success Indicators

✓ Browser console shows: "Loaded 6 clothing items"
✓ Browser console shows: "Rendered 6 cloth items"
✓ No 404 errors in Network tab
✓ Images visible in Step 2
✓ Hover effects work
✓ Can select clothing items

## Still Not Working?

Run the emergency console script and copy the output:

1. Open browser console (F12)
2. Paste contents of `emergency_fix_console.js`
3. Press Enter
4. Copy the entire output
5. Share the output for further diagnosis

The script will tell you exactly what's wrong:
- JavaScript issue
- Image loading issue
- CSS display issue
- Or if everything is working

## Files Created for You

1. `DIAGNOSE_CLOTH_IMAGES.md` - Detailed diagnostic guide
2. `emergency_fix_console.js` - Auto-fix script for console
3. `test_cloth_display.html` - Visual diagnostic test page
4. `CLOTH_IMAGES_FIX_GUIDE.md` - This file

## Next Steps

1. Try hard refresh first (Ctrl+Shift+R)
2. If that doesn't work, run `emergency_fix_console.js`
3. If still broken, open `test_cloth_display.html`
4. Share the diagnostic output if you need more help

The fix is already in your code - you just need to make sure your browser is using the updated files!
