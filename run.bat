@echo off
echo ========================================
echo Tech Support Chatbot - Quick Start
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Starting web server...
echo.
echo Open your browser to: http://localhost:5000
echo Press CTRL+C to stop
echo.

python app.py
