@echo off
REM Setup script for Windows

echo Setting up VTO Backend...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

echo Setup complete!
echo To start the server:
echo   venv\Scripts\activate.bat
echo   python run.py
