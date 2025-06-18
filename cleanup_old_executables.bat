@echo off
title Cleanup Old Executables - Medico-Italiano-IA
echo.
echo ===================================================
echo    🧹 Cleanup Old Executable Files
echo    🏥 Medico-Italiano-IA 🤖
echo ===================================================
echo.

echo This script will remove old executable files to save disk space:
echo.
echo Files to be removed:
echo   📄 dist\Medical_Italian_NER.exe (~3.6GB)
echo   📄 dist\new_medical_ai.exe (~3.6GB)
echo.
echo The new file will be kept:
echo   ✅ dist\Medico-Italiano-IA.exe (~3.6GB)
echo.

set /p choice="Do you want to proceed? (Y/N): "
if /i "%choice%" neq "Y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Removing old executable files...

if exist "dist\Medical_Italian_NER.exe" (
    echo Removing Medical_Italian_NER.exe...
    del /q "dist\Medical_Italian_NER.exe"
    if not exist "dist\Medical_Italian_NER.exe" (
        echo ✅ Medical_Italian_NER.exe removed successfully
    ) else (
        echo ❌ Failed to remove Medical_Italian_NER.exe
    )
) else (
    echo ℹ️ Medical_Italian_NER.exe not found (already removed)
)

if exist "dist\new_medical_ai.exe" (
    echo Removing new_medical_ai.exe...
    del /q "dist\new_medical_ai.exe"
    if not exist "dist\new_medical_ai.exe" (
        echo ✅ new_medical_ai.exe removed successfully
    ) else (
        echo ❌ Failed to remove new_medical_ai.exe
    )
) else (
    echo ℹ️ new_medical_ai.exe not found (already removed)
)

echo.
echo Cleanup completed!
echo.
echo Remaining files in dist folder:
dir /b "dist\*.exe"

echo.
echo 💾 Disk space saved: ~7.2GB
echo 🎯 Active executable: dist\Medico-Italiano-IA.exe
echo.

pause

