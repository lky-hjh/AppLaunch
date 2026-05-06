@echo off
chcp 65001 >nul
cd /d "%~dp0"

:: Try system pythonw first
where pythonw >nul 2>&1
if %errorlevel% == 0 (
    start "" pythonw launcher.py
    exit /b 0
)

:: Fallback to system python
where python >nul 2>&1
if %errorlevel% == 0 (
    start "" python launcher.py
    exit /b 0
)

echo ================================================================
echo  ERROR: Python not found!
echo  Please install Python 3.x from:
echo  https://www.python.org/downloads/
echo ================================================================
pause
