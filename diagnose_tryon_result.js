/**
 * DIAGNOSTIC SCRIPT FOR TRY-ON RESULT NOT SHOWING
 * 
 * INSTRUCTIONS:
 * 1. Open your browser with the app running
 * 2. Press F12 to open Developer Tools
 * 3. Go to "Console" tab
 * 4. Copy and paste this ENTIRE file
 * 5. Press Enter
 * 6. Try clicking "Try On" button
 * 7. Watch the detailed logs
 */

console.log('%c🔍 TRY-ON RESULT DIAGNOSTIC LOADED', 'background: #6366f1; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
console.log('This script will monitor try-on requests and diagnose why results are not showing.\n');

// Store original functions
const originalFetch = window.fetch;
const originalDisplayResult = window.displayResult;

// Track request state
let requestInProgress = false;
let lastRequest = null;
let lastResponse = null;

// Override fetch to monitor API calls
window.fetch = async function(...args) {
    const [url, options] = args;
    
    // Check if this is a try-on request
    if (url && url.includes('/tryon/process')) {
        console.log('%c📤 TRY-ON REQUEST DETECTED', 'background: #3b82f6; color: white; padding: 8px; font-weight: bold;');
        console.log('URL:', url);
        console.log('Method:', options?.method || 'GET');
        
        requestInProgress = true;
        lastRequest = {
            url,
            timestamp: new Date().toISOString(),
            method: options?.method
        };
        
        console.log('⏳ Waiting for response...\n');
    }
    
    // Call original fetch
    const response = await originalFetch(...args);
    
    // Check if this is a try-on response
    if (url && url.includes('/tryon/process')) {
        console.log('%c📥 TRY-ON RESPONSE RECEIVED', 'background: #10b981; color: white; padding: 8px; font-weight: bold;');
        console.log('Status:', response.status, response.statusText);
        console.log('OK:', response.ok);
        
        // Clone response to read it
        const clonedResponse = response.clone();
        
        try {
            const data = await clonedResponse.json();
            lastResponse = data;
            
            console.log('Response Data:', data);
            console.log('\n📊 Response Analysis:');
            console.log('  ✓ Status field:', data.status);
            console.log('  ✓ Image URL field:', data.image_url || data.url || 'MISSING!');
            console.log('  ✓ File ID:', data.file_id);
            console.log('  ✓ Time taken:', data.time_taken);
            
            if (!data.image_url && !data.url) {
                console.error('%c❌ PROBLEM: No image URL in response!', 'background: #ef4444; color: white; padding: 8px; font-weight: bold;');
                console.log('Expected fields: image_url or url');
                console.log('Actual fields:', Object.keys(data));
            } else {
                const imageUrl = data.image_url || data.url;
                console.log('%c✓ Image URL found:', 'color: #10b981; font-weight: bold;', imageUrl);
                
                // Test if image is accessible
                console.log('\n🧪 Testing image accessibility...');
                const fullUrl = imageUrl.startsWith('http') ? imageUrl : `http://localhost:8000${imageUrl}`;
                
                fetch(fullUrl, { method: 'HEAD' })
                    .then(imgResponse => {
                        if (imgResponse.ok) {
                            console.log('%c✓ Image is accessible', 'color: #10b981; font-weight: bold;');
                            console.log('  Status:', imgResponse.status);
                            console.log('  Content-Type:', imgResponse.headers.get('content-type'));
                        } else {
                            console.error('%c❌ Image is NOT accessible', 'background: #ef4444; color: white; padding: 8px;');
                            console.log('  Status:', imgResponse.status);
                            console.log('  This means the file was not saved or static files are not served');
                        }
                    })
                    .catch(error => {
                        console.error('%c❌ Cannot reach image URL', 'background: #ef4444; color: white; padding: 8px;');
                        console.error('  Error:', error.message);
                    });
            }
            
        } catch (error) {
            console.error('%c❌ Failed to parse response JSON', 'background: #ef4444; color: white; padding: 8px;');
            console.error('Error:', error.message);
        }
        
        requestInProgress = false;
        console.log('\n' + '='.repeat(60) + '\n');
    }
    
    return response;
};

// Override displayResult to monitor result display
if (typeof window.displayResult === 'function') {
    window.displayResult = async function(result, timeTaken) {
        console.log('%c🎨 DISPLAY RESULT CALLED', 'background: #8b5cf6; color: white; padding: 8px; font-weight: bold;');
        console.log('Result object:', result);
        console.log('Time taken:', timeTaken);
        
        // Check result section
        const resultSection = document.getElementById('resultSection');
        console.log('\n📋 Result Section Check:');
        console.log('  Exists:', !!resultSection);
        
        if (resultSection) {
            console.log('  Current display:', resultSection.style.display);
            console.log('  Offset height:', resultSection.offsetHeight);
            console.log('  Visible:', resultSection.offsetHeight > 0);
        } else {
            console.error('%c❌ Result section not found in DOM!', 'background: #ef4444; color: white; padding: 8px;');
        }
        
        // Check image URL
        const imageUrl = result.image_url || result.url || result.result_url;
        console.log('\n🖼️  Image URL Check:');
        console.log('  URL:', imageUrl || 'MISSING!');
        
        if (!imageUrl) {
            console.error('%c❌ No image URL in result object!', 'background: #ef4444; color: white; padding: 8px;');
            console.log('Available fields:', Object.keys(result));
        }
        
        // Call original function
        try {
            const returnValue = await originalDisplayResult.call(this, result, timeTaken);
            
            // Check if result section is now visible
            setTimeout(() => {
                console.log('\n✅ Display Result Completed');
                
                if (resultSection) {
                    console.log('Result Section Status:');
                    console.log('  Display:', resultSection.style.display);
                    console.log('  Visible:', resultSection.offsetHeight > 0);
                    
                    if (resultSection.style.display === 'none' || resultSection.offsetHeight === 0) {
                        console.error('%c❌ Result section is still hidden!', 'background: #ef4444; color: white; padding: 8px;');
                        console.log('→ Forcing visibility...');
                        resultSection.style.display = 'block';
                        console.log('✓ Result section forced visible');
                    } else {
                        console.log('%c✓ Result section is visible', 'color: #10b981; font-weight: bold;');
                    }
                }
                
                // Check canvas
                const resultCanvas = document.getElementById('resultCanvas');
                if (resultCanvas) {
                    console.log('\nResult Canvas Status:');
                    console.log('  Display:', resultCanvas.style.display);
                    console.log('  Width:', resultCanvas.width);
                    console.log('  Height:', resultCanvas.height);
                    
                    if (resultCanvas.width === 0 || resultCanvas.height === 0) {
                        console.warn('%c⚠️  Canvas has zero dimensions', 'background: #f59e0b; color: white; padding: 8px;');
                    }
                }
                
                console.log('\n' + '='.repeat(60) + '\n');
            }, 500);
            
            return returnValue;
            
        } catch (error) {
            console.error('%c❌ ERROR IN DISPLAY RESULT', 'background: #ef4444; color: white; padding: 8px; font-weight: bold;');
            console.error('Error:', error);
            console.error('Stack:', error.stack);
            throw error;
        }
    };
    
    console.log('✓ displayResult function monitoring enabled');
} else {
    console.warn('⚠️  displayResult function not found - will monitor fetch only');
}

// Add helper function to manually show result
window.forceShowResult = function(imageUrl) {
    console.log('%c🔧 FORCING RESULT DISPLAY', 'background: #f59e0b; color: white; padding: 8px; font-weight: bold;');
    
    if (!imageUrl && lastResponse) {
        imageUrl = lastResponse.image_url || lastResponse.url;
    }
    
    if (!imageUrl) {
        console.error('No image URL provided and no last response available');
        console.log('Usage: forceShowResult("http://localhost:8000/results/tryon_result_xxx.jpg")');
        return;
    }
    
    const resultSection = document.getElementById('resultSection');
    const resultImage = document.getElementById('resultImage');
    const resultCanvas = document.getElementById('resultCanvas');
    
    if (!resultSection) {
        console.error('Result section not found');
        return;
    }
    
    // Show section
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
    
    // Load image
    if (resultImage) {
        resultImage.src = imageUrl;
        resultImage.style.display = 'block';
        
        if (resultCanvas) {
            resultCanvas.style.display = 'none';
        }
        
        console.log('✓ Result forced to display');
        console.log('Image URL:', imageUrl);
    } else {
        console.error('Result image element not found');
    }
};

// Add helper to check current state
window.checkTryonState = function() {
    console.log('%c📊 CURRENT STATE CHECK', 'background: #6366f1; color: white; padding: 8px; font-weight: bold;');
    
    // Check DOM elements
    const elements = {
        resultSection: document.getElementById('resultSection'),
        resultCanvas: document.getElementById('resultCanvas'),
        resultImage: document.getElementById('resultImage'),
        tryonBtn: document.getElementById('tryonBtn'),
        userImagePreview: document.getElementById('userImagePreview'),
        clothGrid: document.getElementById('clothGrid')
    };
    
    console.log('\n1. DOM Elements:');
    Object.entries(elements).forEach(([name, el]) => {
        console.log(`  ${name}:`, !!el ? '✓ exists' : '✗ missing');
    });
    
    // Check visibility
    if (elements.resultSection) {
        console.log('\n2. Result Section:');
        console.log('  display:', elements.resultSection.style.display);
        console.log('  offsetHeight:', elements.resultSection.offsetHeight);
        console.log('  visible:', elements.resultSection.offsetHeight > 0);
    }
    
    // Check state object
    if (typeof state !== 'undefined') {
        console.log('\n3. Application State:');
        console.log('  userImage:', !!state.userImage);
        console.log('  clothImage:', !!state.clothImage);
        console.log('  selectedCloth:', !!state.selectedCloth);
        console.log('  resultImageUrl:', state.resultImageUrl || 'none');
        console.log('  resultImage:', !!state.resultImage);
    } else {
        console.log('\n3. Application State: Not accessible');
    }
    
    // Check last request/response
    console.log('\n4. Last Try-On Request:');
    if (lastRequest) {
        console.log('  URL:', lastRequest.url);
        console.log('  Time:', lastRequest.timestamp);
    } else {
        console.log('  No request made yet');
    }
    
    console.log('\n5. Last Try-On Response:');
    if (lastResponse) {
        console.log('  Status:', lastResponse.status);
        console.log('  Image URL:', lastResponse.image_url || lastResponse.url || 'missing');
        console.log('  Time taken:', lastResponse.time_taken);
    } else {
        console.log('  No response received yet');
    }
    
    console.log('\n' + '='.repeat(60));
};

// Instructions
console.log('\n📖 DIAGNOSTIC COMMANDS:');
console.log('  checkTryonState()           - Check current state');
console.log('  forceShowResult(url)        - Manually show result image');
console.log('  forceShowResult()           - Show last result (if available)');
console.log('\n💡 Now click "Try On" button and watch the detailed logs!\n');
