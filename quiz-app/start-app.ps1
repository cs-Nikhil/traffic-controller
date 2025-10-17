# Start Quiz App - Windows PowerShell Script

Write-Host "🎯 Starting Online Quiz App..." -ForegroundColor Cyan
Write-Host ""

# Check if MongoDB is running
Write-Host "Checking MongoDB status..." -ForegroundColor Yellow
$mongoService = Get-Service -Name MongoDB -ErrorAction SilentlyContinue

if ($mongoService) {
    if ($mongoService.Status -eq 'Running') {
        Write-Host "✅ MongoDB is running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  MongoDB is not running. Starting MongoDB..." -ForegroundColor Yellow
        Start-Service -Name MongoDB
        Start-Sleep -Seconds 2
        Write-Host "✅ MongoDB started" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  MongoDB service not found. Please start MongoDB manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Cyan

# Start Backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host 'Backend Server' -ForegroundColor Green; npm run dev"

Write-Host "✅ Backend server starting on http://localhost:5000" -ForegroundColor Green
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Starting Frontend..." -ForegroundColor Cyan

# Start Frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; Write-Host 'Frontend Server' -ForegroundColor Green; npm start"

Write-Host "✅ Frontend starting on http://localhost:3000" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Quiz App is starting!" -ForegroundColor Green
Write-Host "Your browser should open automatically." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
