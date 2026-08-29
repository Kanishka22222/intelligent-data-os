$env:Path = "$PSScriptRoot\..\mingit\cmd;" + $env:Path
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Pushing DataOS to GitHub (Clean Initial Commit)  " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
git push -u --force origin main
