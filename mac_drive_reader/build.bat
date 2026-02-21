@echo off
:: ────────────────────────────────────────────────────────────────────
::  Mac Drive Reader – Windows Build Script
::  Run this on a Windows machine to produce a standalone installer.
::
::  Requirements:
::    pip install pyinstaller pytsk3
::    Inno Setup 6 installed (for the installer step)
:: ────────────────────────────────────────────────────────────────────

echo =================================================
echo  Mac Drive Reader – Build
echo =================================================

:: 1. Install dependencies
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
pip install pyinstaller

:: 2. Build the .exe with PyInstaller
echo [2/4] Building executable with PyInstaller...
pyinstaller --onefile ^
            --windowed ^
            --name "MacDriveReader" ^
            --icon "assets\icon.ico" ^
            --add-data "assets;assets" ^
            main.py

if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

echo .exe created at: dist\MacDriveReader.exe

:: 3. Build the Windows installer with Inno Setup (if installed)
echo [3/4] Building Windows installer...
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if exist %ISCC% (
    %ISCC% installer.iss
    echo Installer created at: dist\MacDriveReader_Setup.exe
) else (
    echo [SKIP] Inno Setup not found – skipping installer creation.
    echo Download from: https://jrsoftware.org/isdl.php
)

echo [4/4] Done!
echo.
echo Output files:
echo   dist\MacDriveReader.exe          (standalone, no install needed)
echo   dist\MacDriveReader_Setup.exe    (Windows installer, if Inno Setup was found)
echo.
pause
