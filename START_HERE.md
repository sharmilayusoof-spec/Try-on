# 🚀 Quick Start Guide - Virtual Try-On System

## ✅ Connection Issue FIXED!

The frontend-backend connection issue has been resolved. Follow these steps to test:

---

## Step 1: Start the Backend

Open a terminal and run:

```bash
python run.py
```

You should see:
```
🚀 VTO Backend v1.0.0 starting...
📝 API Documentation: http://0.0.0.0:8000/docs
✅ Server ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The backend must stay running.

---

## Step 2: Open the Frontend

Open `frontend/index.html` in your web browser:

**Option A - Double-click:**
- Navigate to the `frontend` folder
- Double-click `index.html`

**Option B - Live Server (recommended):**
- If using VS Code with Live Server extension
- Right-click `frontend/index.html`
- Select "Open with Live Server"

**Option C - Python HTTP Server:**
```bash
cd frontend
python -m http.server 5500
```
Then open: http://localhost:5500

---

## Step 3: Test the Try-On

1. **Upload Your Photo:**
   - Click the upload area or drag & drop an image
   - Use a photo with a person clearly visible
   - Supported formats: JPG, PNG, WEBP

2. **Select Clothing:**
   - Click on a clothing item from the gallery
   - OR click "Upload Custom Cloth" to use your own

3. **Click "Try On":**
   - The button will show "Processing..."
   - Wait 1-2 seconds
   - Result will appear below!

---

## 🎯 What Was Fixed

### Problem
Frontend was calling `/api/v1/tryon/process` but backend only had `/api/v1/tryon/try-on` (not implemented)

### Solution
1. ✅ Implemented `/process` endpoint with full try-on pipeline
2. ✅ Added `/try-on` as alias for backward compatibility
3. ✅ Updated CORS to allow all origins (development)
4. ✅ Added static file serving for result images
5. ✅ Created test script to verify connection

---

## 📋 Verify Connection (Optional)

Run the test script to verify everything works:

```bash
python test_connection.py
```

Expected output:
```
✅ ALL TESTS PASSED

Your backend is ready!
```

---

## 🐛 Troubleshooting

### "Cannot connect to server"
**Problem:** Backend not running  
**Solution:** Run `python run.py` in a terminal

### "No pose detected"
**Problem:** Person not visible in image  
**Solution:** Use a photo with a person facing the camera

### Frontend not loading
**Problem:** File path issues  
**Solution:** Use Live Server or Python HTTP server (see Step 2)

### Result image not showing
**Problem:** Static files not served  
**Solution:** Already fixed! Make sure backend is running

---

## 📁 Project Structure

```
.
├── app/                          # Backend code
│   ├── api/v1/endpoints/
│   │   └── tryon.py             # ✅ FIXED - /process endpoint
│   ├── core/
│   │   └── config.py            # ✅ FIXED - CORS config
│   ├── main.py                  # ✅ FIXED - Static files
│   └── services/ml/             # ML processing
├── frontend/
│   ├── index.html               # Frontend UI
│   ├── script.js                # API calls
│   └── style.css                # Styling
├── storage/
│   └── results/                 # Generated images
├── run.py                       # Start backend
├── test_connection.py           # ✅ NEW - Test script
└── CONNECTION_FIX_APPLIED.md    # ✅ NEW - Detailed docs
```

---

## 🎨 Features Available

### Phase 1-10 Complete:
- ✅ Modern UI with responsive design
- ✅ Drag & drop image upload
- ✅ Cloth selection gallery
- ✅ Camera integration
- ✅ Real-time mode (1 fps)
- ✅ Multiple view modes (Result, Compare, Side-by-Side)
- ✅ Canvas zoom & pan
- ✅ Toast notifications
- ✅ Error handling
- ✅ Backend API integration

### Backend Processing:
- ✅ Pose detection (MediaPipe)
- ✅ Control point generation
- ✅ TPS cloth warping
- ✅ High-quality overlay
- ✅ Alpha blending
- ✅ Shadow generation
- ✅ Color matching

---

## 📊 API Endpoint

**URL:** `POST http://localhost:8000/api/v1/tryon/process`

**Request:**
```
Content-Type: multipart/form-data

user_image: File
cloth_image: File
```

**Response:**
```json
{
  "status": "success",
  "image_url": "/storage/results/tryon_result_xxx.jpg",
  "time_taken": 1.23,
  "metadata": {
    "person_size": "1024x768",
    "cloth_size": "512x512",
    "landmarks_detected": 33,
    "pose_confidence": 0.75
  }
}
```

---

## 🎯 Next Steps

### For Testing:
1. Start backend: `python run.py`
2. Open frontend: `frontend/index.html`
3. Upload images and try it out!

### For Development:
1. Check `CONNECTION_FIX_APPLIED.md` for detailed changes
2. Review `test_connection.py` for API testing
3. See `FRONTEND_BACKEND_CONNECTION_FIX.md` for diagnosis

### For Production:
1. Update CORS to specific domain
2. Add authentication
3. Use CDN for static files
4. Enable HTTPS
5. Add rate limiting

---

## ✅ Status: READY TO USE!

Everything is configured and working. Just start the backend and open the frontend!

**Questions?** Check the troubleshooting section above or review the detailed documentation in `CONNECTION_FIX_APPLIED.md`.

Happy try-on testing! 🎉
