# PowerShell script to set up the barbershop website

Write-Host "Setting up Elite Barbershop Website..." -ForegroundColor Green

# Create virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env_example.txt" ".env"
    Write-Host "Please edit the .env file with your Google Sheets and email credentials" -ForegroundColor Red
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit the .env file with your credentials" -ForegroundColor White
Write-Host "2. Set up Google Sheets API credentials" -ForegroundColor White
Write-Host "3. Create a Google Sheet for scheduling" -ForegroundColor White
Write-Host "4. Run the application with: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "To start the server: .\.venv\Scripts\Activate.ps1 && python main.py" -ForegroundColor Yellow
