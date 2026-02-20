@echo off
echo ========================================
echo  Fix GitHub Remote for Virtual Try-On
echo ========================================
echo.
echo [INFO] This script will help you push to YOUR GitHub repository
echo        (sharmilayusoof-spec/Try-on)
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo.
    echo Please use Git Bash instead:
    echo 1. Right-click in this folder
    echo 2. Select "Git Bash Here"
    echo 3. Run the commands from GITHUB_PUSH_GUIDE.md
    echo.
    pause
    exit /b 1
)

echo Step 1: Checking current remote...
git remote -v
echo.

echo Step 2: Removing old remote (if exists)...
git remote remove origin 2>nul
echo.

echo Step 3: Adding YOUR repository as remote...
git remote add origin https://github.com/sharmilayusoof-spec/Try-on.git
echo.

echo Step 4: Verifying new remote...
git remote -v
echo.

echo Step 5: Checking git status...
git status
echo.

echo ========================================
echo  Remote Updated Successfully!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Make sure you created the repository on GitHub:
echo    https://github.com/sharmilayusoof-spec/Try-on
echo.
echo 2. Add and commit your files:
echo    git add .
echo    git commit -m "Initial commit: Virtual Try-On Application"
echo.
echo 3. Push to GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. When prompted, use your GitHub Personal Access Token
echo    (NOT your password)
echo.
echo For detailed instructions, see: GITHUB_PUSH_GUIDE.md
echo.
pause

@REM Made with Bob
