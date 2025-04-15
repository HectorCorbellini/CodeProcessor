@echo off
:: Check if running as administrator
echo Checking administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrator privileges to install dependencies.
    echo Please run as administrator.
    pause
    exit /b 1
)

echo.
echo Starting Code Processor Setup...
echo.

:: Create Python virtual environment
echo Creating Python virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment!
    echo Please ensure Python is installed correctly.
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment!
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install required packages!
    pause
    exit /b 1
)

echo.
echo Starting Code Processor...
python main.py

echo.
echo Press any key to exit...
pause
