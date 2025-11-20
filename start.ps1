#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Starts the Kraitif Story Generator Flask application.

.DESCRIPTION
    This script sets up the Python virtual environment, installs dependencies,
    and launches the Flask web server.

.PARAMETER Quickstart
    Skip dependency installation and assume the environment is ready.

.EXAMPLE
    .\start.ps1
    First run - sets up environment and starts server

.EXAMPLE
    .\start.ps1 -Quickstart
    Subsequent runs - skip installation for faster startup
#>

param(
    [switch]$Quickstart,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Show-Usage {
    Write-Host @"
Usage: .\start.ps1 [options]

Options:
  -Quickstart    Skip dependency installation and assume the environment is ready.
  -Help          Show this help message and exit.
"@
}

if ($Help) {
    Show-Usage
    exit 0
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

$VENV_DIR = ".venv"

Write-Info "Starting Kraitif Story Generator..."

if ($Quickstart) {
    Write-Info "Quickstart mode enabled; skipping dependency installation."
}

# Check if virtual environment exists
if (-not (Test-Path $VENV_DIR)) {
    if ($Quickstart) {
        Write-Error-Message "Virtual environment not found at $VENV_DIR. Run without -Quickstart first."
        exit 1
    }
    Write-Warn "Python virtual environment not found at $VENV_DIR. Creating..."
    python -m venv $VENV_DIR
}

# Activate virtual environment
$ActivateScript = Join-Path $VENV_DIR "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    Write-Info "Activating virtual environment..."
    & $ActivateScript
} else {
    Write-Error-Message "Unable to locate activation script at $ActivateScript"
    exit 1
}

# Install dependencies
if (-not $Quickstart) {
    Write-Info "Installing Python dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt

    # Validate required modules
    python -c @"
import importlib
missing = []
for module in ('flask', 'openai'):
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        missing.append(module)

if missing:
    mods = ', '.join(missing)
    raise SystemExit(f'Missing required modules: {mods}. Check requirements.txt installation.')
"@
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} else {
    Write-Warn "Skipping dependency installation; ensure requirements are already satisfied."
}

# Set Flask environment variables
$env:FLASK_APP = if ($env:FLASK_APP) { $env:FLASK_APP } else { "app" }
$env:FLASK_ENV = if ($env:FLASK_ENV) { $env:FLASK_ENV } else { "development" }
$env:FLASK_RUN_PORT = if ($env:FLASK_RUN_PORT) { $env:FLASK_RUN_PORT } else { "8005" }
$env:FLASK_DEBUG = if ($env:FLASK_DEBUG) { $env:FLASK_DEBUG } else { "1" }
$env:PYTHONPATH = if ($env:PYTHONPATH) { $env:PYTHONPATH } else { $SCRIPT_DIR }

Write-Info "Configuration:"
Write-Host "  Python: " -NoNewline -ForegroundColor Blue; Write-Host (Get-Command python).Source
Write-Host "  Virtual env: " -NoNewline -ForegroundColor Blue; Write-Host $VENV_DIR
Write-Host "  FLASK_APP: " -NoNewline -ForegroundColor Blue; Write-Host $env:FLASK_APP
Write-Host "  FLASK_ENV: " -NoNewline -ForegroundColor Blue; Write-Host $env:FLASK_ENV
Write-Host "  FLASK_RUN_PORT: " -NoNewline -ForegroundColor Blue; Write-Host $env:FLASK_RUN_PORT
Write-Host "  FLASK_DEBUG: " -NoNewline -ForegroundColor Blue; Write-Host $env:FLASK_DEBUG

Write-Info "Starting Flask server..."
Write-Info "Open your browser to http://localhost:$($env:FLASK_RUN_PORT)"
Write-Host ""

# Start Flask
if ($env:FLASK_DEBUG -eq "0" -or $env:FLASK_DEBUG -eq "false") {
    python -m flask run --port $env:FLASK_RUN_PORT
} else {
    python -m flask run --debug --port $env:FLASK_RUN_PORT
}
