@echo off
title Code Processor Installer

:: Check if running as administrator
echo Checking administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installer requires administrator privileges to install Python.
    echo Please run as administrator.
    pause
    exit /b 1
)

echo.
echo Starting Code Processor Installer...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Installing Python...
    echo.
    
    :: Download and install Python
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe' -OutFile 'python_installer.exe'"
    if %errorlevel% neq 0 (
        echo Failed to download Python installer!
        echo Please download Python 3.11 manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo.
    echo Running Python installer...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Failed to install Python!
        pause
        exit /b 1
    )
    
    echo.
    echo Python installation complete!
    echo.
)

:: Create Code Processor directory
echo Creating Code Processor directory...
set "CODEPROCESSOR_DIR=%LOCALAPPDATA%\CodeProcessor"
if not exist "%CODEPROCESSOR_DIR%" mkdir "%CODEPROCESSOR_DIR%"

:: Copy files to installation directory
echo Copying files to installation directory...
xcopy /E /I /Y /H . "%CODEPROCESSOR_DIR%"
if %errorlevel% neq 0 (
    echo Failed to copy files!
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "[WScript.Shell]$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\CodeProcessor.lnk'); $shortcut.TargetPath = '%CODEPROCESSOR_DIR%\run_codeprocessor.bat'; $shortcut.WorkingDirectory = '%CODEPROCESSOR_DIR%'; $shortcut.IconLocation = '%CODEPROCESSOR_DIR%\resources\icons\CustomTkinter_icon_Windows.ico'; $shortcut.Save()"

:: Clean up
echo.
echo Installation complete!
echo.
echo Code Processor has been installed to:
echo %CODEPROCESSOR_DIR%
echo.
echo A shortcut has been created on your desktop.
echo.
echo Press any key to exit...
pause
