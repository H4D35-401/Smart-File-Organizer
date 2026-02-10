@echo off
set "SCRIPT_DIR=%~dp0"
set "TARGET_DIR=%USERPROFILE%\Documents\SmartFileOrganizer"

if exist "%TARGET_DIR%\gui.py" (
    echo Starting Configuration...
    python "%TARGET_DIR%\gui.py"
) else (
    echo Error: Smart File Organizer not found in Documents.
    echo Please run install.bat first.
    pause
)
