/**
 * Diagnose and Fix Cloth Images Not Showing
 * 
 * INSTRUCTIONS:
 * 1. Open your app in browser
 * 2. Press F12 to open DevTools
 * 3. Go to Console tab
 * 4. Copy and paste this entire script
 * 5. Press Enter
 * 6. Follow the instructions shown
 */

console.log('%c🔍 CLOTH IMAGES DIAGNOSTIC TOOL', 'font-size: 20px; font-weight: bold; color: #667eea;');
console.log('');

// Step 1: Check if images exist in DOM
console.log('%c📋 STEP 1: Checking DOM', 'font-size: 16px; font-weight: bold;');
const clothImages = document.querySelectorAll('.cloth-image');
const clothItems = document.querySelectorAll('.cloth-item');

console.log(`Found ${clothItems.length} cloth items`);
console.log(`Found ${clothImages.length} cloth images`);

if (clothImages.length === 0) {
    console.error('❌ No images found in DOM!');
    console.log('Problem: Images are not being created');
    console.log('Solution: Check if renderClothGrid() is running');
} else {
    console.log('✓ Images exist in DOM');
}

console.log('');

// Step 2: Check image load status
console.log('%c📸 STEP 2: Checking Image Load Status', 'font-size: 16px; font-weight: bold;');
let loadedCount = 0;
let failedCount = 0;
let pendingCount = 0;

clothImages.forEach((img, i) => {
    const status = {
        index: i,
        src: img.src,
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight
    };
    
    if (img.complete && img.naturalWidth > 0) {
        loadedCount++;
        console.log(`✓ Image ${i}: Loaded (${img.naturalWidth}x${img.naturalHeight}) - ${img.alt}`);
    } else if (img.complete && img.naturalWidth === 0) {
        failedCount++;
        console.error(`✗ Image ${i}: Failed to load - ${img.src}`);
    } else {
        pendingCount++;
        console.warn(`⏳ Image ${i}: Still loading - ${img.alt}`);
    }
});

console.log(`Summary: ${loadedCount} loaded, ${failedCount} failed, ${pendingCount} pending`);
console.log('');

// Step 3: Check dimensions
console.log('%c📏 STEP 3: Checking Image Dimensions', 'font-size: 16px; font-weight: bold;');
let zeroSizeCount = 0;

clothImages.forEach((img, i) => {
    const rect = img.getBoundingClientRect();
    const computed = window.getComputedStyle(img);
    
    if (rect.width === 0 || rect.height === 0) {
        zeroSizeCount++;
        console.error(`✗ Image ${i}: Zero size (${rect.width}x${rect.height})`);
        console.log(`  Computed: width=${computed.width}, height=${computed.height}, flex=${computed.flex}`);
    } else {
        console.log(`✓ Image ${i}: ${rect.width.toFixed(0)}x${rect.height.toFixed(0)}px`);
    }
});

if (zeroSizeCount > 0) {
    console.error(`❌ ${zeroSizeCount} images have zero dimensions!`);
    console.log('This is why images are not visible');
}

console.log('');

// Step 4: Check CSS
console.log('%c🎨 STEP 4: Checking CSS Properties', 'font-size: 16px; font-weight: bold;');
clothImages.forEach((img, i) => {
    const computed = window.getComputedStyle(img);
    const issues = [];
    
    if (computed.display === 'none') issues.push('display:none');
    if (computed.visibility === 'hidden') issues.push('visibility:hidden');
    if (parseFloat(computed.opacity) === 0) issues.push('opacity:0');
    if (computed.flex === '0 1 auto' || computed.flex === 'none') issues.push('flex not set');
    
    if (issues.length > 0) {
        console.error(`✗ Image ${i}: CSS issues - ${issues.join(', ')}`);
    } else {
        console.log(`✓ Image ${i}: CSS OK`);
    }
});

console.log('');

// Step 5: Check parent containers
console.log('%c📦 STEP 5: Checking Parent Containers', 'font-size: 16px; font-weight: bold;');
clothItems.forEach((item, i) => {
    const rect = item.getBoundingClientRect();
    const computed = window.getComputedStyle(item);
    
    if (rect.height === 0) {
        console.error(`✗ Container ${i}: Zero height`);
        console.log(`  Computed: height=${computed.height}, minHeight=${computed.minHeight}`);
    } else {
        console.log(`✓ Container ${i}: ${rect.width.toFixed(0)}x${rect.height.toFixed(0)}px`);
    }
});

console.log('');

// Diagnosis Summary
console.log('%c🎯 DIAGNOSIS SUMMARY', 'font-size: 18px; font-weight: bold; color: #667eea;');
console.log('');

if (clothImages.length === 0) {
    console.error('❌ PROBLEM: No images in DOM');
    console.log('CAUSE: JavaScript not creating images');
    console.log('FIX: Check if renderClothGrid() is being called');
} else if (failedCount > 0) {
    console.error('❌ PROBLEM: Images failed to load');
    console.log('CAUSE: Image files missing or wrong path');
    console.log('FIX: Run "python create_placeholder_images.py"');
} else if (zeroSizeCount > 0) {
    console.error('❌ PROBLEM: Images have zero dimensions');
    console.log('CAUSE: CSS not giving images space');
    console.log('FIX: Apply CSS fix below');
} else {
    console.log('✅ All checks passed! Images should be visible.');
}

console.log('');

// Offer automatic fix
if (zeroSizeCount > 0 || clothImages.length > 0) {
    console.log('%c🔧 AUTOMATIC FIX AVAILABLE', 'font-size: 16px; font-weight: bold; color: #16a34a;');
    console.log('');
    console.log('Run this command to fix CSS issues:');
    console.log('%cfixClothImages()', 'background: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-family: monospace;');
    console.log('');
    
    // Define fix function
    window.fixClothImages = function() {
        console.log('🔧 Applying fixes...');
        
        let fixCount = 0;
        
        // Fix images
        document.querySelectorAll('.cloth-image').forEach((img, i) => {
            img.style.display = 'block';
            img.style.visibility = 'visible';
            img.style.opacity = '1';
            img.style.flex = '1';
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
            fixCount++;
        });
        
        // Fix containers
        document.querySelectorAll('.cloth-item').forEach((item, i) => {
            const rect = item.getBoundingClientRect();
            if (rect.height === 0) {
                item.style.minHeight = '150px';
                item.style.height = 'auto';
            }
        });
        
        console.log(`✓ Applied fixes to ${fixCount} images`);
        console.log('');
        console.log('Check if images are now visible!');
        console.log('If still not visible, run: diagnoseAgain()');
        
        // Define re-diagnose function
        window.diagnoseAgain = function() {
            setTimeout(() => {
                location.reload();
            }, 100);
        };
    };
    
    console.log('Or copy and paste this CSS fix into your style.css:');
    console.log('');
    console.log('%c.cloth-item { min-height: 150px !important; height: auto !important; }', 'background: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-family: monospace;');
    console.log('%c.cloth-image { flex: 1 !important; display: block !important; }', 'background: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-family: monospace;');
}

console.log('');
console.log('%c📝 NEXT STEPS', 'font-size: 16px; font-weight: bold;');
console.log('1. Run fixClothImages() to apply automatic fix');
console.log('2. If that works, add the CSS fix permanently to style.css');
console.log('3. If still not working, check browser console for errors');
console.log('4. Open check_cloth_images.html to test image loading');
console.log('');
