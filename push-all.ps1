# Script to push to all remote repositories
Write-Host "Pushing to all remotes..."

# Push to GitLab
try {
    git push gitlab master
    Write-Host "✓ Pushed to GitLab"
} catch {
    Write-Host "✗ Failed to push to GitLab: $_"
}

# Push to Bitbucket
try {
    git push bitbucket master
    Write-Host "✓ Pushed to Bitbucket"
} catch {
    Write-Host "✗ Failed to push to Bitbucket: $_"
}

# Push to Azure DevOps
try {
    git push azure master
    Write-Host "✓ Pushed to Azure DevOps"
} catch {
    Write-Host "✗ Failed to push to Azure DevOps: $_"
}

Write-Host "Push completed to all available remotes!"

