# Quick Start Guide

## Phase 2 Complete ✓

Your VTO Backend environment is set up and verified!

## What's Working

- Virtual environment created
- FastAPI and core dependencies installed
- Server starts successfully on `http://localhost:8000`
- Configuration management working
- Health check endpoint active

## Start the Server

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the server
python run.py
```

## Test the API

Once running, visit:
- API Root: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Next Steps

Phase 3 will add:
- API skeleton with routing
- Request/response models
- Error handling
- CORS middleware

## ML Dependencies Note

The heavy ML packages (PyTorch, MediaPipe, OpenCV) will be installed in later phases when needed. This keeps the initial setup fast.

To install ML packages now (optional):
```bash
pip install torch torchvision mediapipe opencv-python Pillow numpy
```
