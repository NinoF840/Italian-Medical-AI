@echo off
title Create Medico-Italiano-IA Desktop Shortcut
echo.
echo ===================================================
echo    Creating Desktop Shortcut
echo    🏥 Medico-Italiano-IA 🤖
echo ===================================================
echo.

REM Get current directory
set "CURRENT_DIR=%~dp0"
set "SHORTCUT_NAME=Medico-Italiano-IA.lnk"
set "TARGET_EXE=%CURRENT_DIR%Run_Medico_IA.bat"
set "DESKTOP=%USERPROFILE%\Desktop"

echo Creating desktop shortcut...
echo Target: %TARGET_EXE%
echo Desktop: %DESKTOP%
echo.

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP%\%SHORTCUT_NAME%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%TARGET_EXE%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Medico-Italiano-IA - Advanced Italian Medical AI" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Execute VBS script
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo.
    echo ✅ Success! Desktop shortcut created:
    echo    📂 %DESKTOP%\%SHORTCUT_NAME%
    echo.
    echo You can now double-click the desktop shortcut to launch
    echo Medico-Italiano-IA from anywhere!
) else (
    echo.
    echo ❌ Error: Could not create desktop shortcut
    echo Please check permissions and try running as administrator
)

echo.
echo Press any key to close...
pause >nul

