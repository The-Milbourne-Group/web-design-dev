<#
.SYNOPSIS
    Clones the web-design-dev repository to a local machine, or updates it if
    it is already there.

.DESCRIPTION
    Safe to run repeatedly. Behaviour by target state:
      - missing or empty       -> clone
      - already this repo      -> fetch and fast-forward the current branch
      - non-empty, not this repo -> stop with an error, change nothing

    No credentials are stored or read by this script. Authentication is left to
    git's own credential helper (Git Credential Manager on Windows), which will
    prompt on first use.

.PARAMETER Path
    Destination directory. Default: C:\Users\Matt\.reason

.PARAMETER RepoUrl
    Repository to clone. Default: the web-design-dev origin.

.PARAMETER Branch
    Branch to check out. Default: the repository's default branch.

.EXAMPLE
    .\clone-repo.ps1

.EXAMPLE
    .\clone-repo.ps1 -Path 'D:\work\web-design-dev' -Branch main
#>

[CmdletBinding()]
param(
    [string] $Path    = 'C:\Users\Matt\.reason',
    [string] $RepoUrl = 'https://github.com/The-Milbourne-Group/web-design-dev.git',
    [string] $Branch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]] $Arguments)

    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

# --- Preconditions --------------------------------------------------------

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git was not found on PATH. Install Git for Windows from https://git-scm.com/download/win and reopen PowerShell.'
}

$Path = [System.IO.Path]::GetFullPath($Path)
$parent = Split-Path -Path $Path -Parent
if (-not (Test-Path -LiteralPath $parent)) {
    Write-Host "Creating parent directory $parent"
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

# --- Decide: clone, update, or refuse -------------------------------------

$exists   = Test-Path -LiteralPath $Path
$contents = if ($exists) { @(Get-ChildItem -LiteralPath $Path -Force) } else { @() }

if ($exists -and $contents.Count -gt 0) {

    if (-not (Test-Path -LiteralPath (Join-Path $Path '.git'))) {
        throw "$Path already exists and is not a git repository. Move or remove it first — this script will not overwrite it."
    }

    Push-Location -LiteralPath $Path
    try {
        $origin = (& git remote get-url origin 2>$null)
        if ($LASTEXITCODE -ne 0) { $origin = '' }

        $normalise = { param($u) ($u -replace '\.git$', '').TrimEnd('/').ToLowerInvariant() }
        if ((& $normalise $origin) -ne (& $normalise $RepoUrl)) {
            throw "$Path is a git repository with a different origin ('$origin'). Refusing to touch it."
        }

        $dirty = & git status --porcelain
        if ($dirty) {
            Write-Warning "$Path has uncommitted changes. Fetching only; not updating the working tree."
            Invoke-Git fetch origin --prune
            Write-Host 'Fetched. Commit or stash your changes, then merge manually.'
            return
        }

        Write-Host "Repository already present at $Path — updating."
        Invoke-Git fetch origin --prune
        if ($Branch) { Invoke-Git checkout $Branch }
        Invoke-Git pull --ff-only
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "Cloning $RepoUrl into $Path"
    $cloneArgs = @('clone', $RepoUrl, $Path)
    if ($Branch) { $cloneArgs += @('--branch', $Branch) }
    Invoke-Git @cloneArgs
}

# --- Report ---------------------------------------------------------------

Push-Location -LiteralPath $Path
try {
    $branchName = (& git rev-parse --abbrev-ref HEAD).Trim()
    $commit     = (& git log -1 --pretty='format:%h %s').Trim()
    Write-Host ''
    Write-Host "Done. $Path"
    Write-Host "  branch: $branchName"
    Write-Host "  head:   $commit"
}
finally {
    Pop-Location
}
