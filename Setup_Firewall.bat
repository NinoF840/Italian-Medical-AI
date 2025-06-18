@echo off
title Medico-Italiano-IA - Firewall Setup
echo.
echo ===================================================
echo    🔥 Medico-Italiano-IA Firewall Setup
echo    Configuring Windows Firewall for Port 8501
echo ===================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Error: This script requires administrator privileges
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo 🔧 Configuring Windows Firewall for Medico-Italiano-IA...
echo.

REM Remove existing rules if they exist
netsh advfirewall firewall delete rule name="Medico-Italiano-IA Inbound" >nul 2>&1
netsh advfirewall firewall delete rule name="Medico-Italiano-IA Outbound" >nul 2>&1

REM Add inbound rule for port 8501
echo Adding inbound firewall rule for port 8501...
netsh advfirewall firewall add rule name="Medico-Italiano-IA Inbound" dir=in action=allow protocol=TCP localport=8501 program="%~dp0dist\Medico-Italiano-IA.exe"

if %errorLevel% equ 0 (
    echo ✅ Inbound rule added successfully
) else (
    echo ❌ Failed to add inbound rule
    goto :error
)

REM Add outbound rule for port 8501
echo Adding outbound firewall rule for port 8501...
netsh advfirewall firewall add rule name="Medico-Italiano-IA Outbound" dir=out action=allow protocol=TCP localport=8501 program="%~dp0dist\Medico-Italiano-IA.exe"

if %errorLevel% equ 0 (
    echo ✅ Outbound rule added successfully
) else (
    echo ❌ Failed to add outbound rule
    goto :error
)

echo.
echo ✅ Firewall configuration completed successfully!
echo.
echo 📝 Created firewall rules:
echo    - Medico-Italiano-IA Inbound (TCP port 8501)
echo    - Medico-Italiano-IA Outbound (TCP port 8501)
echo.
echo 🚀 You can now run Medico-Italiano-IA without firewall issues.
echo.
pause
exit /b 0

:error
echo.
echo ❌ Firewall configuration failed!
echo Please check your administrator privileges and try again.
echo.
pause
exit /b 1

