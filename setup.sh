#!/bin/bash
# Setup script for Unix/Linux/Mac

echo "Setting up VTO Backend..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Setup complete!"
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python run.py"
