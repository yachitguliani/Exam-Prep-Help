# Check if .venv exists
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Activate venv
Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "Installing dependencies..."
python -m pip install -r requirements.txt

# Run Agent
Write-Host "Starting ExamPrep Agent..."
python main.py
