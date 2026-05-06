@echo off
chcp 65001 >nul
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% == 0 (
    start "" pythonw launcher.py
    exit /b 0
)

where python >nul 2>&1
if %errorlevel% == 0 (
    start "" python launcher.py
    exit /b 0
)

echo ================================================================
echo  ERROR: Python not found!
echo  Please install Python 3.x from:
echo  https://www.python.org/downloads/
echo  (Remember to check "Add Python to PATH")
echo ================================================================
pause
