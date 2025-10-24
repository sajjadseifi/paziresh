<#
----------------------------------------
 Django Run Script (Professional Edition)
 Author: Sajad Seifi Lor
----------------------------------------
#>

Write-Host "🔹 Checking environment..." -ForegroundColor Cyan
if (!(Test-Path "env")) {
    Write-Host "[ERROR] Virtual environment 'env' not found!" -ForegroundColor Red
    Write-Host "Please create it first using: python -m venv env"
    exit
}

Write-Host "`n🔹 Activating virtual environment..." -ForegroundColor Cyan
& env\Scripts\Activate.ps1

if (-not $?) {
    Write-Host "[ERROR] Failed to activate virtual environment." -ForegroundColor Red
    exit
}

$port = Read-Host "Enter port (default 8000)"
if ([string]::IsNullOrWhiteSpace($port)) { $port = 8000 }

Write-Host "`n🚀 Starting Django server on http://127.0.0.1:$port ..." -ForegroundColor Green
Start-Process "http://127.0.0.1:$port"
python manage.py runserver $port

deactivate
Write-Host "`n✅ Server stopped. Virtual environment deactivated." -ForegroundColor Yellow
