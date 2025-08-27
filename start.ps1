# PowerShell script to start the barbershop website

Write-Host "Starting Elite Barbershop Website..." -ForegroundColor Green

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "Virtual environment not found. Running setup..." -ForegroundColor Yellow
    .\setup.ps1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env_example.txt" ".env"
    Write-Host "Please edit the .env file with your credentials before running again" -ForegroundColor Red
    exit
}

# Start the server
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "The website will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python main.py
