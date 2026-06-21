param(
    [string]$Message = "update app"
)

Set-Location $PSScriptRoot

$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to commit - working tree is clean." -ForegroundColor Yellow
    exit 0
}

Write-Host "Staging changes..." -ForegroundColor Cyan
git add -A
if (-not $?) { Write-Host "git add failed." -ForegroundColor Red; exit 1 }

Write-Host "Committing: $Message" -ForegroundColor Cyan
git commit -m $Message
if (-not $?) { Write-Host "git commit failed." -ForegroundColor Red; exit 1 }

Write-Host "Pushing to main..." -ForegroundColor Cyan
git push
if (-not $?) { Write-Host "git push failed." -ForegroundColor Red; exit 1 }

Write-Host "Deployed. GitHub Pages will update in ~1 minute." -ForegroundColor Green
Write-Host "https://milo9.github.io/dsny-trivia/" -ForegroundColor DarkGray
