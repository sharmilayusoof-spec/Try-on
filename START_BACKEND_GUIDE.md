# Start Backend Server - Quick Guide

## Error Message
"Cannot connect to server. Please ensure the backend is running on http://localhost:8000"

## This Means
The FastAPI backend server is not running or not accessible.

## Quick Fix

### Step 1: Open Terminal/Command Prompt
Navigate to your project root directory (where `app/` folder is located).

### Step 2: Start Backend Server

**Option 1: Using uvicorn (Recommended)**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using Python module**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: If uvicorn not installed**
```bash
pip install uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify Server is Running

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 4: Test Backend

Open browser and go to:
- http://localhost:8000 - Should show a response
- http://localhost:8000/docs - Should show API documentation

## Common Issues

### Issue 1: "uvicorn: command not found"

**Fix:** Install uvicorn
```bash
pip install uvicorn[standard]
```

### Issue 2: "No module named 'app'"

**Fix:** Make sure you're in the project root directory (not inside `app/` folder)
```bash
# Check current directory
pwd  # Linux/Mac
cd   # Windows

# Should show path ending with project name, not /app
# If inside app/, go back one level:
cd ..
```

### Issue 3: "Port 8000 is already in use"

**Fix:** Kill the process using port 8000

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

Then update frontend to use port 8001 in `frontend/script.js`:
```javascript
const CONFIG = {
    apiBaseUrl: 'http://localhost:8001',  // Change from 8000 to 8001
    // ...
};
```

### Issue 4: Missing Dependencies

**Fix:** Install all required packages
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install fastapi uvicorn python-multipart pillow opencv-python numpy mediapipe
```

### Issue 5: Python Version Issues

**Fix:** Ensure Python 3.8+ is installed
```bash
python --version
# Should show Python 3.8 or higher

# If not, install Python 3.8+ and use:
python3 -m uvicorn app.main:app --reload
```

## Verification Steps

### 1. Check if Backend is Running
```bash
# In a new terminal, test the backend:
curl http://localhost:8000
```

Should return a response (not connection refused).

### 2. Check API Endpoints
```bash
# Test health endpoint (if exists)
curl http://localhost:8000/api/v1/tryon/process -X OPTIONS
```

Should return CORS headers, not 404.

### 3. Check from Browser
Open browser console (F12) and run:
```javascript
fetch('http://localhost:8000/api/v1/tryon/process', { method: 'OPTIONS' })
  .then(response => console.log('Backend OK:', response.ok))
  .catch(error => console.error('Backend Error:', error));
```

Should log "Backend OK: true".

## Complete Startup Checklist

- [ ] Navigate to project root directory
- [ ] Activate virtual environment (if using one)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start backend: `uvicorn app.main:app --reload`
- [ ] Verify server shows "Application startup complete"
- [ ] Test http://localhost:8000 in browser
- [ ] Open frontend and test try-on

## Keep Backend Running

The backend must stay running while you use the frontend. You should see:
- Terminal window with uvicorn logs
- Logs appear when you make requests
- No errors in the logs

## If Still Not Working

### Check Project Structure
Your project should look like:
```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── results/
└── requirements.txt
```

### Check app/main.py Exists
```bash
# Should show the file
ls app/main.py
```

### Check Python Path
```bash
# Should include current directory
python -c "import sys; print(sys.path)"
```

## Quick Start Script

Create a file `start_backend.sh` (Linux/Mac) or `start_backend.bat` (Windows):

**Linux/Mac (start_backend.sh):**
```bash
#!/bin/bash
echo "Starting Virtual Try-On Backend..."
cd "$(dirname "$0")"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Make executable:
```bash
chmod +x start_backend.sh
./start_backend.sh
```

**Windows (start_backend.bat):**
```batch
@echo off
echo Starting Virtual Try-On Backend...
cd /d "%~dp0"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
```

Run:
```batch
start_backend.bat
```

## Expected Output When Working

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then when you make a request:
```
INFO:     127.0.0.1:xxxxx - "POST /api/v1/tryon/process HTTP/1.1" 200 OK
```

## Stop Backend

Press `Ctrl+C` in the terminal where backend is running.

---

**TL;DR:** Run `uvicorn app.main:app --reload` from project root directory.
