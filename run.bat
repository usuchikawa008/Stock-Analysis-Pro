@echo off
echo ====================================
echo   Stock Analysis Pro
echo   Starting application...
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    echo.
)

REM Run the Streamlit app
echo Starting Stock Analysis Pro...
echo.
streamlit run app.py

pause
