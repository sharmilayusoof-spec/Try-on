@echo off
echo ========================================
echo  Virtual Try-On Backend Server
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: app\main.py not found!
    echo Please run this script from the project root directory.
    echo.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo.
    pause
    exit /b 1
)

echo.
echo Checking uvicorn installation...
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo WARNING: uvicorn not found. Installing...
    pip install uvicorn[standard]
    if errorlevel 1 (
        echo ERROR: Failed to install uvicorn
        pause
        exit /b 1
    )
)

echo.
echo Creating results directory...
if not exist "results" mkdir results

echo.
echo ========================================
echo  Starting Backend Server...
echo ========================================
echo.
echo Server will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
