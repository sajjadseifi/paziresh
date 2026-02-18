@echo off

REM ======= Project directory (current location of this BAT file) =======
SET PROJECT_DIR=%~dp0

REM ======= Virtualenv path =======
SET VENV_DIR=C:\repositroy\venvs\prod-paziresh

REM ======= Server settings =======
SET PORT=8000
SET IP=0.0.0.0

REM ======= Detect Local IPv4 =======
FOR /F "tokens=14 delims= " %%A IN ('ipconfig ^| findstr /R /C:"IPv4.*: [0-9]"') DO SET LOCAL_IP=%%A

echo Run Django server with virtualenv activated
echo Auto-detect your local IPv4 for mobile access
echo. 

echo    [1]  Development Information   
echo            Project directory   :       %PROJECT_DIR%
echo            Virtualenv path     :       %VENV_DIR%
echo            Server will run on  :       %IP%:%PORT%
echo            Your local IPv4 is  :       %LOCAL_IP%
echo. 

call %VENV_DIR%\Scripts\activate.bat

echo    [2] HOW TO CONNECT FROM PHONE
echo            1. Starting Django server on http://127.0.0.1:%PORT%
echo            2. Make sure your phone and PC are on the same Wi-Fi network.
echo            3. Open your phone browser and go to:
echo.   
echo                  http://%LOCAL_IP%:%PORT%
echo.   
echo            This is the correct IP for external access.
echo. 

echo    [3] Run Server ALMAHDI APP 
echo            Please Wait...

python devops.py --dev %IP%:%PORT% 
pause
