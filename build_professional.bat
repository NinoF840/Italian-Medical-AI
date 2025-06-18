@echo off
echo ================================
echo BUILDING PROFESSIONAL VERSION
echo Medico-Italiano-IA Professional
echo ================================
echo.

echo [1/4] Cleaning previous builds...
if exist "dist\Medico-Italiano-IA-Professional.exe" del "dist\Medico-Italiano-IA-Professional.exe"
if exist "build" rmdir /s /q "build"

echo [2/4] Activating environment...
REM Activate conda environment if needed
REM call conda activate your_env_name

echo [3/4] Building Professional executable...
echo This may take 10-15 minutes...
pyinstaller --clean Medico-Italiano-IA-Professional.spec

echo [4/4] Checking build result...
if exist "dist\Medico-Italiano-IA-Professional.exe" (
    echo.
    echo ✅ SUCCESS! Professional version built successfully!
    echo.
    echo 📁 Location: dist\Medico-Italiano-IA-Professional.exe
    echo 📊 Size: 
    dir "dist\Medico-Italiano-IA-Professional.exe" | find "Medico-Italiano-IA-Professional.exe"
    echo.
    echo ✅ PROFESSIONAL VERSION FEATURES:
    echo    🚀 Unlimited requests
    echo    📝 Unlimited text length
    echo    🎯 All advanced features enabled
    echo    👨‍💻 Owner/Developer mode
    echo    🔓 No watermarks or limitations
    echo.
    echo 🏃‍♂️ Ready to run: double-click the exe or use Run_Professional.bat
) else (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    echo 💡 Common fixes:
    echo    - Make sure you have PyInstaller installed: pip install pyinstaller
    echo    - Check that app_professional.py exists
    echo    - Ensure all dependencies are installed: pip install -r requirements.txt
)

echo.
echo ================================
echo Build process complete!
echo ================================
pause

