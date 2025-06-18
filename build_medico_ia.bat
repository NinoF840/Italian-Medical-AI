@echo off
echo Building Medico-Italiano-IA Executable...
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\Medico-Italiano-IA" rmdir /s /q "build\Medico-Italiano-IA"
if exist "dist\Medico-Italiano-IA.exe" del /q "dist\Medico-Italiano-IA.exe"
echo.

REM Build new executable
echo Building new executable with PyInstaller...
pyinstaller --clean Medico-Italiano-IA.spec

REM Check if build was successful
if exist "dist\Medico-Italiano-IA.exe" (
    echo.
    echo ✅ Build successful!
    echo ✅ Executable created: dist\Medico-Italiano-IA.exe
    echo.
    echo File size:
    dir "dist\Medico-Italiano-IA.exe" | findstr "Medico-Italiano-IA.exe"
    echo.
    echo 🚀 Ready to run: dist\Medico-Italiano-IA.exe
) else (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    echo.
)

pause

