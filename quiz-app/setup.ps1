# Quiz App Setup Script for Windows PowerShell

Write-Host "🎯 Online Quiz App - Setup Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check MongoDB
Write-Host "Checking MongoDB installation..." -ForegroundColor Yellow
try {
    $mongoVersion = mongod --version
    Write-Host "✅ MongoDB is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  MongoDB not found. Please install MongoDB from https://www.mongodb.com/try/download/community" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

# Setup Backend
Set-Location backend
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
    
    Write-Host "Seeding database with sample questions..." -ForegroundColor Yellow
    npm run seed
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database seeded successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Database seeding failed. Make sure MongoDB is running." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

Set-Location ..

Write-Host ""
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Setup Frontend
Set-Location frontend
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    exit 1
}

Set-Location ..

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "1. Open a terminal and run: cd backend && npm run dev" -ForegroundColor White
Write-Host "2. Open another terminal and run: cd frontend && npm start" -ForegroundColor White
Write-Host ""
Write-Host "The app will open at http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Happy Quizzing! 🎉" -ForegroundColor Cyan
