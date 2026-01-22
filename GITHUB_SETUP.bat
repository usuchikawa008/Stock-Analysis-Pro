@echo off
echo ============================================
echo   GitHub Repository Setup
echo   Stock Analysis Pro - Vietnam
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo OR use GitHub Desktop: https://desktop.github.com/
    pause
    exit /b 1
)

echo Git is installed! Continuing...
echo.

REM Initialize git repository
echo [1/5] Initializing Git repository...
git init

REM Add all files
echo.
echo [2/5] Adding all files...
git add .

REM Commit
echo.
echo [3/5] Creating initial commit...
git commit -m "Initial commit - Stock Analysis Pro VN"

REM Instructions
echo.
echo [4/5] Next steps:
echo ============================================
echo.
echo 1. Go to GitHub.com and create a new repository
echo    URL: https://github.com/new
echo.
echo 2. Name it: stock-analysis-vn (or any name you like)
echo.
echo 3. DO NOT initialize with README (we already have one)
echo.
echo 4. After creating, copy the repository URL
echo    It looks like: https://github.com/USERNAME/stock-analysis-vn.git
echo.
echo 5. Then run these commands:
echo.
echo    git remote add origin YOUR_REPO_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo ============================================
echo.
echo OR use GitHub Desktop for easier setup!
echo Download: https://desktop.github.com/
echo.

pause
