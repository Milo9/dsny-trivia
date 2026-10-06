param(
    [string]$Message = "update app",
    # Multi-line messages (e.g. with a Co-Authored-By trailer): write them to a
    # file OUTSIDE this repo and pass -MessageFile, since 'git add -A' would
    # sweep a same-repo message file into the commit.
    [string]$MessageFile,
    # Untracked files abort the deploy by default so stray scratch files never
    # get swept into a commit. Pass this once you've checked the list.
    [switch]$IncludeUntracked,
    [switch]$SkipChecks,
    # Runs the version bump/sync and the gates, then stops before git add.
    [switch]$DryRun
)

# Keep this file pure ASCII: Windows PowerShell 5.1 reads a BOM-less script as
# ANSI, so curly quotes or dashes would corrupt it.

Set-Location $PSScriptRoot
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$appJs     = Join-Path $PSScriptRoot 'app.js'
$indexHtml = Join-Path $PSScriptRoot 'index.html'

function Fail($msg) { Write-Host $msg -ForegroundColor Red; exit 1 }

$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to commit - working tree is clean." -ForegroundColor Yellow
    exit 0
}

# --- Untracked-file guard ------------------------------------------------------
$untracked = @(git ls-files --others --exclude-standard)
if ($untracked.Count -gt 0 -and -not $IncludeUntracked) {
    Write-Host "Untracked files would be committed:" -ForegroundColor Yellow
    $untracked | ForEach-Object { Write-Host "  $_" }
    Fail "Move/delete anything that isn't part of this change, or re-run with -IncludeUntracked."
}

$changed = @(git diff --name-only HEAD) + $untracked

# --- Version bump + cache-busting sync -------------------------------------------
# Any code change bumps APP_VERSION (minor +1) unless it was already bumped by
# hand in this change; then every ?v= in index.html is synced to it. The
# app.js?v= value is what the in-app update toast compares, so this is what
# tells already-open apps that a new build exists.
$codeFiles = @('app.js', 'style.css', 'storage.js', 'game-logic.js', 'index.html')
$codeChanged = @($changed | Where-Object { $codeFiles -contains $_ }).Count -gt 0

$appText = [System.IO.File]::ReadAllText($appJs)
$verRegex = "const APP_VERSION = '(\d+)\.(\d+)';"
$m = [regex]::Match($appText, $verRegex)
if (-not $m.Success) { Fail "Couldn't find APP_VERSION in app.js." }
$version = "$($m.Groups[1].Value).$($m.Groups[2].Value)"

if ($codeChanged) {
    $headApp = (git show HEAD:app.js) -join "`n"
    $hm = [regex]::Match($headApp, $verRegex)
    $headVersion = if ($hm.Success) { "$($hm.Groups[1].Value).$($hm.Groups[2].Value)" } else { "" }
    if ($version -eq $headVersion) {
        $major = [int]$m.Groups[1].Value
        $minor = [int]$m.Groups[2].Value + 1
        $version = "$major.$minor"
        $appText = [regex]::Replace($appText, $verRegex, "const APP_VERSION = '$version';")
        [System.IO.File]::WriteAllText($appJs, $appText, $utf8NoBom)
        Write-Host "Bumped APP_VERSION $headVersion -> $version" -ForegroundColor Cyan
    } else {
        Write-Host "APP_VERSION already bumped to $version in this change" -ForegroundColor Cyan
    }
}

$html = [System.IO.File]::ReadAllText($indexHtml)
$synced = [regex]::Replace($html, '(\.(?:js|css)\?v=)[^"'']+', ('${1}' + $version))
if ($synced -ne $html) {
    [System.IO.File]::WriteAllText($indexHtml, $synced, $utf8NoBom)
    Write-Host "Synced index.html ?v= strings to $version" -ForegroundColor Cyan
}
$vs = [regex]::Matches([System.IO.File]::ReadAllText($indexHtml), '\.(?:js|css)\?v=([^"'']+)') | ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique
if (@($vs).Count -ne 1 -or $vs -ne $version) { Fail "index.html ?v= strings don't all match APP_VERSION $version : $($vs -join ', ')" }

# --- Gates -----------------------------------------------------------------------
if (-not $SkipChecks) {
    if (@($changed | Where-Object { $_ -like 'questions/*' }).Count -gt 0) {
        Write-Host "Validating question corpus..." -ForegroundColor Cyan
        python scripts/validate_corpus.py
        if ($LASTEXITCODE -ne 0) { Fail "Corpus validation failed - fix the errors above before deploying." }
    }
    if (Get-Command node -ErrorAction SilentlyContinue) {
        Write-Host "Running unit tests..." -ForegroundColor Cyan
        $testOut = node --test --test-reporter=dot test/game-logic.test.js
        $testCode = $LASTEXITCODE
        $testOut | ForEach-Object { Write-Host "  $_" }
        if ($testCode -ne 0) { Fail "Unit tests failed - run 'node --test test/game-logic.test.js' for details." }
    } else {
        Write-Host "node not found - skipping unit tests." -ForegroundColor Yellow
    }
}

if ($DryRun) {
    Write-Host "Dry run complete (v$version) - nothing staged or committed." -ForegroundColor Green
    exit 0
}

# --- Commit + push ----------------------------------------------------------------
Write-Host "Staging changes..." -ForegroundColor Cyan
git add -A
if ($LASTEXITCODE -ne 0) { Fail "git add failed." }

if ($MessageFile) {
    if (-not (Test-Path $MessageFile)) { Fail "Message file not found: $MessageFile" }
    Write-Host "Committing (message from $MessageFile)" -ForegroundColor Cyan
    git commit -F $MessageFile
} else {
    Write-Host "Committing: $Message" -ForegroundColor Cyan
    git commit -m $Message
}
if ($LASTEXITCODE -ne 0) { Fail "git commit failed." }

Write-Host "Pushing to main..." -ForegroundColor Cyan
git push
if ($LASTEXITCODE -ne 0) { Fail "git push failed." }

Write-Host "Deployed v$version. GitHub Pages will update in ~1 minute." -ForegroundColor Green
Write-Host "https://milo9.github.io/dsny-trivia/" -ForegroundColor DarkGray
