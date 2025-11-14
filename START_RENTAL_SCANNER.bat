@echo off
REM rentFalcon - One-Click Launcher
REM Newmarket Edition - Version 2.1

title rentFalcon - Newmarket

echo.
echo ========================================
echo    RENTFALCON - NEWMARKET
echo ========================================
echo.
echo Starting up...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/4] Python detected...

REM Check if we're in the right directory
if not exist "app.py" (
    echo ERROR: Cannot find app.py
    echo Please run this file from the rental-scanner folder.
    echo.
    pause
    exit /b 1
)

echo [2/4] Project files found...

REM Check if required packages are installed
python -c "import flask, requests, bs4, selenium" >nul 2>&1
if errorlevel 1 (
    echo [3/4] Installing required packages (first time only)...
    echo This may take 2-3 minutes...
    echo.
    python -m pip install --quiet --user Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install packages.
        echo Please check your internet connection and try again.
        echo.
        pause
        exit /b 1
    )
    echo Packages installed successfully!
) else (
    echo [3/4] Required packages already installed...
)

echo [4/4] Starting Rental Scanner...
echo.
echo ========================================
echo    RENTFALCON IS STARTING
echo ========================================
echo.
echo The web browser will open automatically in 5 seconds...
echo Default location: Newmarket, Ontario
echo.
echo NOTE: First search may take 30-60 seconds
echo       (ChromeDriver download - one time only)
echo.
echo ========================================
echo.
echo To stop the server, press Ctrl+C
echo Then close this window.
echo.
echo ========================================
echo.

REM Wait 3 seconds then open browser
timeout /t 3 >nul
start http://localhost:5000

REM Start the Flask application
python app.py

REM If the app exits, pause so user can see any error messages
echo.
echo.
echo ========================================
echo rentFalcon has stopped.
echo ========================================
echo.
pause
