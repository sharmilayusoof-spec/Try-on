/**
 * EMERGENCY FIX FOR CLOTH IMAGES NOT SHOWING
 * 
 * INSTRUCTIONS:
 * 1. Open your browser (with the app running)
 * 2. Press F12 to open Developer Tools
 * 3. Go to "Console" tab
 * 4. Copy and paste this ENTIRE file into the console
 * 5. Press Enter
 * 
 * This will diagnose and fix the issue automatically.
 */

console.log('%c🔧 EMERGENCY CLOTH IMAGE FIX', 'background: #6366f1; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
console.log('Starting diagnostic and repair...\n');

// Step 1: Check if images exist in DOM
console.log('Step 1: Checking DOM...');
const images = document.querySelectorAll('.cloth-image');
const containers = document.querySelectorAll('.cloth-item');

console.log(`Found ${images.length} cloth images`);
console.log(`Found ${containers.length} cloth containers`);

if (images.length === 0) {
    console.error('❌ No cloth images found in DOM!');
    console.log('→ Possible causes:');
    console.log('  1. JavaScript not loaded');
    console.log('  2. clothes.json failed to load');
    console.log('  3. renderClothes() not called');
    console.log('\n→ Try refreshing the page (Ctrl+Shift+R)');
} else {
    console.log('✓ Images found in DOM\n');
}

// Step 2: Check image loading status
console.log('Step 2: Checking image loading...');
let loadedCount = 0;
let failedCount = 0;

images.forEach((img, i) => {
    const loaded = img.complete && img.naturalWidth > 0;
    if (loaded) {
        loadedCount++;
        console.log(`✓ Image ${i + 1}: ${img.alt} (${img.naturalWidth}x${img.naturalHeight})`);
    } else {
        failedCount++;
        console.error(`❌ Image ${i + 1}: ${img.alt} - FAILED TO LOAD`);
        console.log(`   Source: ${img.src}`);
    }
});

console.log(`\nLoaded: ${loadedCount}/${images.length}`);
if (failedCount > 0) {
    console.error(`Failed: ${failedCount}/${images.length}`);
    console.log('→ Check Network tab for 404 errors\n');
} else {
    console.log('✓ All images loaded successfully\n');
}

// Step 3: Check display dimensions
console.log('Step 3: Checking display dimensions...');
let visibleCount = 0;
let invisibleCount = 0;

images.forEach((img, i) => {
    const displayWidth = img.offsetWidth;
    const displayHeight = img.offsetHeight;
    const visible = displayWidth > 0 && displayHeight > 0;
    
    if (visible) {
        visibleCount++;
        console.log(`✓ Image ${i + 1}: ${img.alt} - ${displayWidth}x${displayHeight}px`);
    } else {
        invisibleCount++;
        console.error(`❌ Image ${i + 1}: ${img.alt} - ${displayWidth}x${displayHeight}px (INVISIBLE!)`);
    }
});

console.log(`\nVisible: ${visibleCount}/${images.length}`);
if (invisibleCount > 0) {
    console.error(`Invisible: ${invisibleCount}/${images.length}`);
    console.log('→ This is a CSS dimension issue!\n');
} else {
    console.log('✓ All images are visible\n');
}

// Step 4: Check CSS properties
console.log('Step 4: Checking CSS properties...');
if (images.length > 0) {
    const testImg = images[0];
    const testContainer = containers[0];
    
    const imgStyles = window.getComputedStyle(testImg);
    const containerStyles = window.getComputedStyle(testContainer);
    
    console.log('Container (.cloth-item) CSS:');
    console.log(`  display: ${containerStyles.display}`);
    console.log(`  flex-direction: ${containerStyles.flexDirection}`);
    console.log(`  min-height: ${containerStyles.minHeight}`);
    console.log(`  height: ${containerStyles.height}`);
    
    console.log('\nImage (.cloth-image) CSS:');
    console.log(`  display: ${imgStyles.display}`);
    console.log(`  flex: ${imgStyles.flex}`);
    console.log(`  width: ${imgStyles.width}`);
    console.log(`  height: ${imgStyles.height}`);
    console.log(`  object-fit: ${imgStyles.objectFit}`);
    
    // Check for issues
    const issues = [];
    if (containerStyles.display !== 'flex') issues.push('Container display is not flex');
    if (containerStyles.flexDirection !== 'column') issues.push('Container flex-direction is not column');
    if (containerStyles.minHeight !== '150px') issues.push('Container min-height is not 150px');
    if (!imgStyles.flex.includes('1')) issues.push('Image flex is not set to 1');
    if (imgStyles.display !== 'block') issues.push('Image display is not block');
    
    if (issues.length > 0) {
        console.error('\n❌ CSS Issues Found:');
        issues.forEach(issue => console.error(`  - ${issue}`));
        console.log('\n→ Applying emergency CSS fix...\n');
    } else {
        console.log('\n✓ All CSS properties are correct\n');
    }
}

// Step 5: Apply emergency fix if needed
if (invisibleCount > 0) {
    console.log('%c🚨 APPLYING EMERGENCY FIX', 'background: #ef4444; color: white; padding: 8px; font-weight: bold;');
    
    // Remove any existing emergency fix
    const existingFix = document.getElementById('emergency-cloth-fix');
    if (existingFix) existingFix.remove();
    
    // Add emergency CSS
    const style = document.createElement('style');
    style.id = 'emergency-cloth-fix';
    style.textContent = `
        /* Emergency fix for cloth images */
        .cloth-item {
            min-height: 150px !important;
            height: auto !important;
            display: flex !important;
            flex-direction: column !important;
            overflow: hidden !important;
        }
        
        .cloth-image {
            flex: 1 !important;
            display: block !important;
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            min-height: 100px !important;
        }
        
        .cloth-label {
            flex-shrink: 0 !important;
        }
    `;
    document.head.appendChild(style);
    
    console.log('✓ Emergency CSS applied!');
    console.log('→ Images should now be visible');
    console.log('→ If not, try hard refresh: Ctrl+Shift+R\n');
    
    // Force re-render
    setTimeout(() => {
        console.log('Checking if fix worked...');
        let fixedCount = 0;
        images.forEach((img, i) => {
            const displayWidth = img.offsetWidth;
            const displayHeight = img.offsetHeight;
            if (displayWidth > 0 && displayHeight > 0) {
                fixedCount++;
            }
        });
        
        if (fixedCount === images.length) {
            console.log('%c✓ FIX SUCCESSFUL!', 'background: #10b981; color: white; padding: 8px; font-weight: bold;');
            console.log(`All ${fixedCount} images are now visible!`);
        } else {
            console.error('%c❌ FIX INCOMPLETE', 'background: #ef4444; color: white; padding: 8px; font-weight: bold;');
            console.log(`Only ${fixedCount}/${images.length} images are visible`);
            console.log('\n→ Next steps:');
            console.log('  1. Hard refresh: Ctrl+Shift+R');
            console.log('  2. Clear browser cache');
            console.log('  3. Check if you\'re viewing the correct HTML file');
            console.log('  4. Open test_cloth_display.html for detailed diagnostics');
        }
    }, 500);
} else if (images.length > 0 && visibleCount === images.length) {
    console.log('%c✓ NO FIX NEEDED', 'background: #10b981; color: white; padding: 8px; font-weight: bold;');
    console.log('All images are loading and displaying correctly!');
} else if (images.length === 0) {
    console.log('%c⚠️ CANNOT FIX', 'background: #f59e0b; color: white; padding: 8px; font-weight: bold;');
    console.log('No images found in DOM. This is a JavaScript loading issue.');
    console.log('\n→ Next steps:');
    console.log('  1. Check browser console for JavaScript errors');
    console.log('  2. Verify clothes.json is loading');
    console.log('  3. Check if renderClothes() function exists');
    console.log('  4. Hard refresh: Ctrl+Shift+R');
}

// Step 6: Provide summary
console.log('\n' + '='.repeat(60));
console.log('DIAGNOSTIC SUMMARY');
console.log('='.repeat(60));
console.log(`Images in DOM: ${images.length}`);
console.log(`Images loaded: ${loadedCount}/${images.length}`);
console.log(`Images visible: ${visibleCount}/${images.length}`);

if (images.length > 0 && loadedCount === images.length && visibleCount === images.length) {
    console.log('\n✅ STATUS: ALL WORKING');
} else if (images.length === 0) {
    console.log('\n❌ STATUS: JAVASCRIPT ISSUE');
} else if (loadedCount < images.length) {
    console.log('\n❌ STATUS: IMAGE LOADING ISSUE');
} else if (visibleCount < images.length) {
    console.log('\n❌ STATUS: CSS DISPLAY ISSUE (FIXED)');
}

console.log('='.repeat(60));
console.log('\nFor detailed testing, open: test_cloth_display.html');
console.log('For step-by-step guide, read: DIAGNOSE_CLOTH_IMAGES.md');
