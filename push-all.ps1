#!/usr/bin/env pwsh

# Script to push to all git remotes
# Usage: .\push-all.ps1 [branch-name]
# If no branch is specified, uses current branch

param(
    [string]$Branch = ""
)

# Get current branch if not specified
if ([string]::IsNullOrEmpty($Branch)) {
    $Branch = git rev-parse --abbrev-ref HEAD
    Write-Host "Using current branch: $Branch" -ForegroundColor Green
}

# List of remotes to push to
$remotes = @("azure", "bitbucket", "gitlab")

# Track success/failure
$results = @{}

Write-Host "Starting push to all remotes..." -ForegroundColor Yellow
Write-Host "Branch: $Branch" -ForegroundColor Cyan
Write-Host ""

foreach ($remote in $remotes) {
    Write-Host "Pushing to $remote..." -ForegroundColor Blue
    
    try {
        # Push to remote
        $output = git push $remote $Branch 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Successfully pushed to $remote" -ForegroundColor Green
            $results[$remote] = "SUCCESS"
        } else {
            Write-Host "✗ Failed to push to $remote" -ForegroundColor Red
            Write-Host "Error: $output" -ForegroundColor Red
            $results[$remote] = "FAILED: $output"
        }
    }
    catch {
        Write-Host "✗ Exception occurred pushing to $remote" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        $results[$remote] = "EXCEPTION: $($_.Exception.Message)"
    }
    
    Write-Host ""
}

# Summary
Write-Host "=== PUSH SUMMARY ===" -ForegroundColor Yellow
foreach ($remote in $remotes) {
    $status = $results[$remote]
    if ($status -eq "SUCCESS") {
        Write-Host "${remote}: ✓ SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "${remote}: ✗ $status" -ForegroundColor Red
    }
}
Write-Host ""

# Set upstream for azure if it was successful
if ($results["azure"] -eq "SUCCESS") {
    Write-Host "Setting azure as upstream for branch $Branch..." -ForegroundColor Blue
    git branch --set-upstream-to=azure/$Branch $Branch 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Azure set as upstream" -ForegroundColor Green
    }
}

Write-Host "Push operation completed!" -ForegroundColor Yellow

