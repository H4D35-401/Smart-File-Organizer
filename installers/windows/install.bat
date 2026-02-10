@echo off
set "SCRIPT_DIR=%~dp0"
set "SRC_DIR=%SCRIPT_DIR%..\..\src"
set "TARGET_DIR=%USERPROFILE%\Documents\SmartFileOrganizer"

echo --- Installing Smart File Organizer (Windows) ---

echo [*] Installing dependencies...
pip install watchdog

echo [*] Creating project directory...
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
xcopy /E /I /Y "%SRC_DIR%" "%TARGET_DIR%"

echo [*] Creating startup script...
set "VBS_SCRIPT=%TARGET_DIR%\run_hidden.vbs"
(
echo Set WshShell = CreateObject("WScript.Shell"^) 
echo WshShell.Run chr(34^) ^& "%TARGET_DIR%\organizer.py" ^& chr(34^), 0
echo Set WshShell = Nothing
) > "%VBS_SCRIPT%"

echo [*] Adding to Startup...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_SCRIPT=%temp%\create_shortcut.vbs"

(
echo Set oWS = WScript.CreateObject("WScript.Shell"^)
echo sLinkFile = "%STARTUP_FOLDER%\SmartFileOrganizer.lnk"
echo Set oLink = oWS.CreateShortcut(sLinkFile^)
echo oLink.TargetPath = "wscript.exe"
echo oLink.Arguments = chr(34^) ^& "%VBS_SCRIPT%" ^& chr(34^)
echo oLink.WorkingDirectory = "%TARGET_DIR%"
echo oLink.Save
) > "%SHORTCUT_SCRIPT%"

cscript /nologo "%SHORTCUT_SCRIPT%"
del "%SHORTCUT_SCRIPT%"

echo --- Done! Re-run this script if you move the folder. ---
pause
