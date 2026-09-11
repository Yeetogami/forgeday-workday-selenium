$ErrorActionPreference = "Stop"
if (-not $env:WORKDAY_HEADLESS) { $env:WORKDAY_HEADLESS = "false" }
python -m pytest
if (Test-Path "reports\report.html") { start "reports\report.html" }
