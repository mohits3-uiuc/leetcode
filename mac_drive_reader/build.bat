@echo off
setlocal enabledelayedexpansion
:: ──────────────────────────────────────────────────────────────────────
::  Mac Drive Reader – Windows Build Script
::  Produces:  dist\MacDriveReader.exe          (single portable .exe)
::             dist\MacDriveReader_Setup.exe    (one-click installer)
::
::  Requirements (all installed automatically by this script):
::    Python 3.10+   https://www.python.org/downloads/
::    Inno Setup 6   https://jrsoftware.org/isdl.php  (for installer step)
:: ──────────────────────────────────────────────────────────────────────

echo.
echo ================================================
echo   Mac Drive Reader  –  Build
echo ================================================
echo.

:: ── Step 1: Install Python dependencies ──────────────────────────────
echo [1/3]  Installing Python dependencies...
pip install --quiet --upgrade pytsk3 apfs construct pyinstaller
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is in PATH.
    pause & exit /b 1
)

:: ── Step 2: Build single-file .exe with PyInstaller ──────────────────
echo [2/3]  Building MacDriveReader.exe  (single file, no Python required)...

:: Clean previous build
if exist build   rmdir /s /q build
if exist dist\MacDriveReader.exe del /q dist\MacDriveReader.exe

:: Use the .spec file for a fully configured build
pyinstaller --clean --noconfirm MacDriveReader.spec

if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause & exit /b 1
)
echo.
echo  Built:  dist\MacDriveReader.exe
echo.

:: ── Step 3: Build one-click Windows installer with Inno Setup ─────────
echo [3/3]  Building one-click installer...

set ISCC1="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set ISCC2="C:\Program Files\Inno Setup 6\ISCC.exe"

if exist %ISCC1% (
    %ISCC1% installer.iss
) else if exist %ISCC2% (
    %ISCC2% installer.iss
) else (
    echo [SKIP] Inno Setup 6 not found.
    echo        Download from: https://jrsoftware.org/isdl.php
    echo        Then re-run this script to generate the Setup.exe.
    goto done
)

echo.
echo  Built:  dist\MacDriveReader_Setup.exe

:done
echo.
echo ================================================
echo   Build complete!
echo.
echo   Portable .exe ........  dist\MacDriveReader.exe
echo   One-click installer ..  dist\MacDriveReader_Setup.exe
echo ================================================
echo.
pause
echo Output files:
echo   dist\MacDriveReader.exe          (standalone, no install needed)
echo   dist\MacDriveReader_Setup.exe    (Windows installer, if Inno Setup was found)
echo.
pause
