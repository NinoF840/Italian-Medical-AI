@echo off
title Port 8501 Accessibility Test
echo.
echo ===================================================
echo    🔍 Port 8501 Accessibility Test
echo    Testing Medico-Italiano-IA Network Setup
echo ===================================================
echo.

echo 🔧 Checking Windows Firewall rules...
echo.

REM Check for inbound rule
netsh advfirewall firewall show rule name="Medico-Italiano-IA Inbound" >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Inbound firewall rule exists
) else (
    echo ❌ Inbound firewall rule NOT found
    echo 💡 Run Setup_Firewall.bat as Administrator
)

REM Check for outbound rule
netsh advfirewall firewall show rule name="Medico-Italiano-IA Outbound" >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Outbound firewall rule exists
) else (
    echo ❌ Outbound firewall rule NOT found
    echo 💡 Run Setup_Firewall.bat as Administrator
)

echo.
echo 🌐 Testing port 8501 accessibility...
echo.

REM Check if port is currently in use
netstat -ano | findstr :8501 >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ Port 8501 is currently in use (application might be running)
    echo.
    echo 📋 Current connections on port 8501:
    netstat -ano | findstr :8501
) else (
    echo ℹ️  Port 8501 is currently free (normal when app is not running)
)

echo.
echo 🖥️  System Information:
echo.
echo OS: 
systeminfo | findstr /B /C:"OS Name"
echo RAM:
systeminfo | findstr /B /C:"Total Physical Memory"
echo Available RAM:
systeminfo | findstr /B /C:"Available Physical Memory"

echo.
echo 📁 File Check:
if exist "dist\Medico-Italiano-IA.exe" (
    echo ✅ Medico-Italiano-IA.exe found
    for %%A in ("dist\Medico-Italiano-IA.exe") do echo    Size: %%~zA bytes
) else (
    echo ❌ Medico-Italiano-IA.exe NOT found in dist folder
)

if exist "Setup_Firewall.bat" (
    echo ✅ Setup_Firewall.bat available
) else (
    echo ❌ Setup_Firewall.bat NOT found
)

if exist "VISITOR_SETUP_GUIDE.md" (
    echo ✅ VISITOR_SETUP_GUIDE.md available
) else (
    echo ❌ VISITOR_SETUP_GUIDE.md NOT found
)

echo.
echo ===================================================
echo 🎯 Test Complete
echo.
echo Next steps:
echo 1. If firewall rules missing: Run Setup_Firewall.bat as Admin
echo 2. If files missing: Check installation integrity
echo 3. If issues persist: See VISITOR_SETUP_GUIDE.md
echo 4. For support: Email nino58150@gmail.com
echo ===================================================
echo.
pause

