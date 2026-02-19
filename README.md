# AI-Powered Virtual Try-On Backend

Backend system for virtual clothing try-on using computer vision and deep learning.

## Features

- User image upload and processing
- Clothing image upload
- Pose detection using MediaPipe
- Human segmentation
- Cloth warping and overlay
- Real-time inference optimization

## Tech Stack

- **Framework:** FastAPI
- **ML:** PyTorch, MediaPipe
- **Image Processing:** OpenCV, Pillow
- **Storage:** Local filesystem

## Project Structure

```
vto-backend/
├── app/              # Application code
├── storage/          # File storage
├── tests/            # Test suite
└── requirements.txt  # Dependencies
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

**Option 1: Automated Setup**

For Windows:
```bash
setup.bat
```

For Unix/Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

**Option 2: Manual Setup**

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate.bat`
   - Unix/Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

1. Activate virtual environment (if not already active)
2. Run the server:
```bash
python run.py
```

The server will start at `http://localhost:8000`

## API Documentation

Once running, visit: `http://localhost:8000/docs`

## Development

Built following clean architecture principles with phase-by-phase development.
