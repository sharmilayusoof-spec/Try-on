/**
 * Quick test script to check if images are visible
 * Paste this into browser console
 */

console.log('🔍 Testing Image Visibility...\n');

// Test 1: Check if images exist
const images = document.querySelectorAll('.cloth-image');
console.log(`✓ Found ${images.length} images in DOM`);

if (images.length === 0) {
    console.error('❌ No images found! Check if renderClothGrid() is running.');
} else {
    // Test 2: Check load status
    let loadedCount = 0;
    images.forEach((img, i) => {
        if (img.complete && img.naturalWidth > 0) {
            loadedCount++;
            console.log(`  ✓ Image ${i}: Loaded (${img.naturalWidth}x${img.naturalHeight})`);
        } else {
            console.error(`  ✗ Image ${i}: Not loaded`);
        }
    });
    
    console.log(`\n✓ ${loadedCount}/${images.length} images loaded successfully\n`);
    
    // Test 3: Check dimensions
    console.log('📏 Checking Display Dimensions...\n');
    let visibleCount = 0;
    images.forEach((img, i) => {
        const rect = img.getBoundingClientRect();
        const isVisible = rect.width > 0 && rect.height > 0;
        
        if (isVisible) {
            visibleCount++;
            console.log(`  ✓ Image ${i}: ${rect.width.toFixed(0)}x${rect.height.toFixed(0)}px - VISIBLE`);
        } else {
            console.error(`  ✗ Image ${i}: ${rect.width}x${rect.height}px - HIDDEN (zero size)`);
        }
    });
    
    console.log(`\n${visibleCount}/${images.length} images are visible\n`);
    
    // Test 4: Check CSS
    console.log('🎨 Checking CSS Properties...\n');
    images.forEach((img, i) => {
        const computed = window.getComputedStyle(img);
        const issues = [];
        
        if (computed.display === 'none') issues.push('display:none');
        if (computed.visibility === 'hidden') issues.push('visibility:hidden');
        if (parseFloat(computed.opacity) === 0) issues.push('opacity:0');
        if (computed.width === '0px') issues.push('width:0');
        if (computed.height === '0px') issues.push('height:0');
        
        if (issues.length > 0) {
            console.error(`  ✗ Image ${i}: CSS issues - ${issues.join(', ')}`);
        } else {
            console.log(`  ✓ Image ${i}: CSS OK (display:${computed.display}, opacity:${computed.opacity})`);
        }
    });
    
    // Test 5: Check parent containers
    console.log('\n📦 Checking Parent Containers...\n');
    const items = document.querySelectorAll('.cloth-item');
    items.forEach((item, i) => {
        const rect = item.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) {
            console.error(`  ✗ Container ${i}: Zero size (${rect.width}x${rect.height})`);
        } else {
            console.log(`  ✓ Container ${i}: ${rect.width.toFixed(0)}x${rect.height.toFixed(0)}px`);
        }
    });
    
    // Summary
    console.log('\n' + '='.repeat(50));
    console.log('SUMMARY');
    console.log('='.repeat(50));
    
    if (visibleCount === images.length) {
        console.log('✅ ALL IMAGES ARE VISIBLE!');
        console.log('Your fix is working correctly.');
    } else {
        console.error('❌ SOME IMAGES ARE NOT VISIBLE');
        console.log('\nPossible fixes:');
        console.log('1. Add to CSS: .cloth-item { min-height: 150px; }');
        console.log('2. Add to CSS: .cloth-image { flex: 1; display: block; }');
        console.log('3. Run: document.querySelectorAll(".cloth-image").forEach(img => img.style.flex = "1")');
        console.log('\nOr open debug_invisible_images.html and click "Apply Quick Fix"');
    }
    console.log('');
}
