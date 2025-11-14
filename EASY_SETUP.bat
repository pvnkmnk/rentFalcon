@echo off
REM rentFalcon - Easy Setup for First-Time Users
REM Newmarket Edition - Version 2.1
REM This script will set up everything you need automatically!

title rentFalcon - Easy Setup

color 0A
echo.
echo ========================================================================
echo.
echo     RENTFALCON - NEWMARKET EDITION
echo     Easy Setup Wizard
echo.
echo ========================================================================
echo.
echo This setup wizard will:
echo   [1] Check if Python is installed
echo   [2] Check if Google Chrome is installed
echo   [3] Install all required software packages
echo   [4] Test the installation
echo   [5] Create a desktop shortcut (optional)
echo   [6] Launch the Rental Scanner
echo.
echo This will take about 3-5 minutes.
echo.
echo ========================================================================
echo.
pause

echo.
echo ========================================================================
echo STEP 1: Checking Python Installation
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [X] PYTHON NOT FOUND!
    echo.
    echo Python is required to run rentFalcon.
    echo.
    echo Please follow these steps:
    echo   1. Go to: https://www.python.org/downloads/
    echo   2. Download Python 3.8 or newer
    echo   3. Run the installer
    echo   4. IMPORTANT: Check "Add Python to PATH" during installation
    echo   5. After installation, restart this computer
    echo   6. Run this setup again
    echo.
    echo Press any key to open Python download page...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% detected
echo.

echo ========================================================================
echo STEP 2: Checking Google Chrome Installation
echo ========================================================================
echo.

REM Check for Chrome in common locations
set CHROME_FOUND=0
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set CHROME_FOUND=1

if %CHROME_FOUND%==0 (
    color 0E
    echo [!] CHROME NOT FOUND
    echo.
    echo Google Chrome is required for the Rentals.ca scraper.
    echo The app will still work with Kijiji listings, but you'll
    echo get fewer results without Chrome.
    echo.
    echo Would you like to:
    echo   [1] Continue without Chrome (fewer results)
    echo   [2] Install Chrome first (recommended)
    echo.
    choice /c 12 /n /m "Enter your choice (1 or 2): "
    if errorlevel 2 (
        echo.
        echo Opening Chrome download page...
        echo After installing Chrome, run this setup again.
        echo.
        pause
        start https://www.google.com/chrome/
        exit /b 1
    )
    echo.
    echo [!] Continuing without Chrome...
    echo.
) else (
    echo [OK] Google Chrome detected
    echo.
)

echo ========================================================================
echo STEP 3: Installing Required Packages
echo ========================================================================
echo.
echo This may take 2-3 minutes depending on your internet speed...
echo Please be patient and do not close this window.
echo.

REM Check if packages are already installed
python -c "import flask, requests, bs4, selenium, webdriver_manager, apscheduler" >nul 2>&1
if not errorlevel 1 (
    echo [OK] All packages are already installed!
    echo.
    goto :skip_install
)

echo Installing packages...
echo.

REM Install packages with progress messages
echo [1/6] Installing Flask (web framework)...
python -m pip install --quiet --user Flask Flask-SQLAlchemy >nul 2>&1
if errorlevel 1 goto :install_error

echo [2/6] Installing web scraping tools...
python -m pip install --quiet --user requests beautifulsoup4 >nul 2>&1
if errorlevel 1 goto :install_error

echo [3/6] Installing browser automation...
python -m pip install --quiet --user selenium >nul 2>&1
if errorlevel 1 goto :install_error

echo [4/6] Installing ChromeDriver manager...
python -m pip install --quiet --user webdriver-manager >nul 2>&1
if errorlevel 1 goto :install_error

echo [5/6] Installing task scheduler...
python -m pip install --quiet --user APScheduler >nul 2>&1
if errorlevel 1 goto :install_error

echo [6/6] Installing configuration tools...
python -m pip install --quiet --user python-dotenv >nul 2>&1
if errorlevel 1 goto :install_error

echo.
echo [OK] All packages installed successfully!
echo.

:skip_install

echo ========================================================================
echo STEP 4: Testing Installation
echo ========================================================================
echo.
echo Running system verification...
echo.

python -c "import sys; import flask; import requests; import bs4; import selenium; from scrapers.scraper_manager import ScraperManager; print('[OK] All components verified!'); print('[OK] Flask version:', flask.__version__); print('[OK] Selenium version:', selenium.__version__); print('[OK] Python version:', sys.version.split()[0]); manager = ScraperManager(); print('[OK] Scrapers loaded:', ', '.join(manager.get_enabled_scrapers()))" 2>nul
if errorlevel 1 (
    color 0C
    echo [X] Verification failed!
    echo.
    echo There may be an issue with the installation.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Installation verified successfully!
echo.

echo ========================================================================
echo STEP 5: Creating Desktop Shortcut (Optional)
echo ========================================================================
echo.
echo Would you like to create a desktop shortcut for easy access?
echo.
choice /c YN /n /m "Create desktop shortcut? (Y/N): "
if errorlevel 2 goto :skip_shortcut

echo.
echo Creating desktop shortcut...

REM Get the current directory
set "SCRIPT_DIR=%~dp0"

REM Get the desktop path
for /f "tokens=3*" %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%i %%j"
if not defined DESKTOP set "DESKTOP=%USERPROFILE%\Desktop"
call set "DESKTOP=%DESKTOP%"

REM Create shortcut using VBScript
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\rentFalcon - Newmarket.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%START_RENTAL_SCANNER.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "rentFalcon - Find rentals in Newmarket area" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,1" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs" >nul 2>&1
del "%TEMP%\CreateShortcut.vbs"

if exist "%DESKTOP%\rentFalcon - Newmarket.lnk" (
    echo [OK] Desktop shortcut created!
) else (
    echo [!] Could not create shortcut, but app is ready to use.
)
echo.

:skip_shortcut

echo ========================================================================
echo STEP 6: Setup Complete!
echo ========================================================================
echo.
color 0A
echo   _____ _    _  _____ _____ ______  _____ _____ _
echo  / ____^| ^|  ^| ^|/ ____/ ____^|  ____^|/ ____/ ____^| ^|
echo ^| (___ ^| ^|  ^| ^| ^|   ^| ^|    ^| ^|__  ^| ^|   ^| (___ ^| ^|
echo  \___ \^| ^|  ^| ^| ^|   ^| ^|    ^|  __^| ^| ^|    \___ \^| ^|
echo  ____) ^| ^|__^| ^| ^|___^| ^|____^| ^|____^| ^|___ ____) ^|_^|
echo ^|_____/ \____/ \_____\_____^|______^|\_____|_____/(_)
echo.
echo.
echo Setup is complete! Here's what you can do now:
echo.
echo OPTION 1: Launch now
echo   Press any key to start Rental Scanner immediately
echo.
echo OPTION 2: Launch later
if exist "%DESKTOP%\rentFalcon - Newmarket.lnk" (
    echo   Double-click "rentFalcon - Newmarket" on your desktop
) else (
    echo   Double-click "START_RENTAL_SCANNER.bat" in this folder
)
echo.
echo ========================================================================
echo.
echo QUICK START GUIDE:
echo   1. The app will open in your web browser automatically
echo   2. Default location is set to: Newmarket, Ontario
echo   3. Enter your price range (optional)
echo   4. Click "Search Rentals"
echo   5. Wait 10-15 seconds for results
echo.
echo NOTE: First search may take 30-60 seconds while ChromeDriver downloads
echo       (this is a one-time setup, subsequent searches are fast)
echo.
echo SUPPORTED CITIES (within 25 km of Newmarket):
echo   - Newmarket, Aurora, Richmond Hill, Bradford
echo   - East Gwillimbury, Markham, Vaughan, King City
echo.
echo ========================================================================
echo.
echo Press any key to launch Rental Scanner now...
pause >nul

echo.
echo Starting rentFalcon...
echo.
timeout /t 2 >nul

REM Launch the app
call START_RENTAL_SCANNER.bat
exit /b 0

:install_error
color 0C
echo.
echo [X] ERROR: Failed to install packages
echo.
echo This could be due to:
echo   - No internet connection
echo   - Firewall blocking Python
echo   - Insufficient permissions
echo.
echo Troubleshooting:
echo   1. Check your internet connection
echo   2. Try running as Administrator (right-click, "Run as administrator")
echo   3. Temporarily disable antivirus/firewall
echo   4. Make sure Python was installed with "Add to PATH" checked
echo.
echo If problems persist, try manual installation:
echo   pip install Flask Flask-SQLAlchemy requests beautifulsoup4 selenium webdriver-manager python-dotenv APScheduler
echo.
pause
exit /b 1
