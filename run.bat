@echo off
setlocal enabledelayedexpansion

:: ----------------------------------------
:: Django Run Script (Professional Edition)
:: Author: Sajad Seifi Lor
:: ----------------------------------------

title Django Project Runner
color 0A

if not exist "env\" (
    echo [ERROR] Virtual environment 'env' not found!
    echo Please create it first using: python -m venv env
    pause
    exit /b
)

echo.
echo 🔹 Activating virtual environment...
call env\Scripts\activate

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b
)

set /p PORT=Enter port (default 8000): 
if "%PORT%"=="" set PORT=8000

echo.
echo 🚀 Starting Django server on http://127.0.0.1:%PORT% ...
start "" "http://127.0.0.1:%PORT%"
python manage.py runserver %PORT%

deactivate
echo ✅ Server stopped. Virtual environment deactivated.
pause
