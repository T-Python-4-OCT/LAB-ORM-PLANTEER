$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$pythonPath = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path $pythonPath)) {
    py -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Install Python 3.11+ from python.org, then run this script again.' }
    & $pythonPath -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
}
& $pythonPath manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Database migration failed.' }
& $pythonPath manage.py seed_plants
& $pythonPath manage.py runserver 127.0.0.1:8000
