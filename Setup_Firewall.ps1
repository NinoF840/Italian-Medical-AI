# Medico-Italiano-IA Firewall Setup (PowerShell)
# Configures Windows Firewall to allow port 8501

param(
    [switch]$Force
)

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "   🔥 Medico-Italiano-IA Firewall Setup" -ForegroundColor White
Write-Host "   Configuring Windows Firewall for Port 8501" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Error: This script requires administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

$ExePath = Join-Path $PSScriptRoot "dist\Medico-Italiano-IA.exe"

# Check if executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "❌ Error: Medico-Italiano-IA.exe not found at:" -ForegroundColor Red
    Write-Host "   $ExePath" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "🔧 Configuring Windows Firewall for Medico-Italiano-IA..." -ForegroundColor Green
Write-Host ""

try {
    # Remove existing rules if they exist
    Write-Host "Removing existing firewall rules..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName "Medico-Italiano-IA*" -ErrorAction SilentlyContinue
    
    # Add inbound rule
    Write-Host "Adding inbound firewall rule for port 8501..." -ForegroundColor Blue
    New-NetFirewallRule -DisplayName "Medico-Italiano-IA Inbound" `
                        -Direction Inbound `
                        -Protocol TCP `
                        -LocalPort 8501 `
                        -Action Allow `
                        -Program $ExePath `
                        -Profile Any `
                        -Description "Allow Medico-Italiano-IA to receive connections on port 8501"
    
    Write-Host "✅ Inbound rule added successfully" -ForegroundColor Green
    
    # Add outbound rule
    Write-Host "Adding outbound firewall rule for port 8501..." -ForegroundColor Blue
    New-NetFirewallRule -DisplayName "Medico-Italiano-IA Outbound" `
                        -Direction Outbound `
                        -Protocol TCP `
                        -LocalPort 8501 `
                        -Action Allow `
                        -Program $ExePath `
                        -Profile Any `
                        -Description "Allow Medico-Italiano-IA to make connections on port 8501"
    
    Write-Host "✅ Outbound rule added successfully" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "✅ Firewall configuration completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Created firewall rules:" -ForegroundColor Cyan
    Write-Host "   - Medico-Italiano-IA Inbound (TCP port 8501)" -ForegroundColor White
    Write-Host "   - Medico-Italiano-IA Outbound (TCP port 8501)" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 You can now run Medico-Italiano-IA without firewall issues." -ForegroundColor Green
    
    # Test port availability
    Write-Host ""
    Write-Host "🔍 Testing port availability..." -ForegroundColor Yellow
    $portTest = Test-NetConnection -ComputerName "localhost" -Port 8501 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($portTest) {
        Write-Host "✅ Port 8501 is accessible" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Port 8501 is not currently in use (this is normal when app is not running)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Firewall configuration failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "   1. Ensure you're running as Administrator" -ForegroundColor White
    Write-Host "   2. Check if Windows Firewall service is running" -ForegroundColor White
    Write-Host "   3. Verify the executable path is correct" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to exit"

