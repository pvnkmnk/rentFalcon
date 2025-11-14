@echo off
REM Create Desktop Shortcut for Rental Scanner
REM This will create an easy-to-use icon on your desktop

title Create Desktop Shortcut

echo.
echo ========================================
echo   RENTAL SCANNER - SHORTCUT CREATOR
echo ========================================
echo.
echo This will create a shortcut on your desktop
echo for easy access to the Rental Scanner.
echo.

REM Get the current directory (where the batch file is located)
set "SCRIPT_DIR=%~dp0"

REM Get the desktop path
for /f "tokens=3*" %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%i %%j"
if not defined DESKTOP set "DESKTOP=%USERPROFILE%\Desktop"

REM Expand environment variables in desktop path
call set "DESKTOP=%DESKTOP%"

REM Create PowerShell script to make the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\Rental Scanner - Newmarket.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%SCRIPT_DIR%START_RENTAL_SCANNER.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Rental Scanner - Find rentals in Newmarket area" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%%SystemRoot%%\System32\imageres.dll,1" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Execute the VBScript
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

if exist "%DESKTOP%\Rental Scanner - Newmarket.lnk" (
    echo.
    echo ========================================
    echo    SUCCESS!
    echo ========================================
    echo.
    echo Desktop shortcut created successfully!
    echo.
    echo Location: %DESKTOP%
    echo Name: "Rental Scanner - Newmarket"
    echo.
    echo You can now:
    echo   1. Close this window
    echo   2. Double-click the desktop icon
    echo   3. Start finding rentals!
    echo.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo    ERROR
    echo ========================================
    echo.
    echo Failed to create desktop shortcut.
    echo You can still use START_RENTAL_SCANNER.bat
    echo directly from this folder.
    echo.
    echo ========================================
)

echo.
pause
