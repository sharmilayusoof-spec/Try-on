#!/bin/bash

echo "========================================"
echo " Virtual Try-On Backend Server"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "ERROR: app/main.py not found!"
    echo "Please run this script from the project root directory."
    echo ""
    exit 1
fi

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.8 or higher"
        echo ""
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD --version

echo ""
echo "Checking uvicorn installation..."
if ! $PYTHON_CMD -c "import uvicorn" 2>/dev/null; then
    echo "WARNING: uvicorn not found. Installing..."
    $PYTHON_CMD -m pip install uvicorn[standard]
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install uvicorn"
        exit 1
    fi
fi

echo ""
echo "Creating results directory..."
mkdir -p results

echo ""
echo "========================================"
echo " Starting Backend Server..."
echo "========================================"
echo ""
echo "Server will run on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

$PYTHON_CMD -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
