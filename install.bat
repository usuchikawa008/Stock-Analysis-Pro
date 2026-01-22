@echo off
echo ====================================
echo   Stock Analysis Pro - Installation
echo ====================================
echo.

REM Upgrade pip first
echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

REM Install basic requirements
echo.
echo [2/3] Installing required packages...
pip install yfinance pandas numpy ta requests

REM Install Streamlit (optional)
echo.
echo [3/3] Installing Streamlit (optional, for UI version)...
pip install streamlit plotly

echo.
echo ====================================
echo   Installation Complete!
echo ====================================
echo.
echo You can now run:
echo   - Console version: python console_app.py
echo   - UI version: streamlit run app.py
echo.
pause
