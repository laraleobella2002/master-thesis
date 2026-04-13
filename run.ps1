param(
    [string]$Script = "laras_experiment_correction.py"
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$scriptPath = Join-Path $projectRoot $Script

if (-not (Test-Path $pythonExe)) {
    Write-Error "Virtual environment not found at '.venv'. Run setup first."
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Host "Script '$Script' was not found in the project root." -ForegroundColor Red
    Write-Host ""
    Write-Host "Available .py files:" -ForegroundColor Yellow
    Get-ChildItem -Path $projectRoot -Filter "*.py" | Select-Object -ExpandProperty Name
    exit 1
}

Write-Host "Running $Script with local virtual environment..." -ForegroundColor Green
& $pythonExe $scriptPath
$exitCode = $LASTEXITCODE
if ($null -ne $exitCode -and $exitCode -ne 0) {
    exit $exitCode
}
