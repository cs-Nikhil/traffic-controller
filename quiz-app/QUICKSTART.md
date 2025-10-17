# 🚀 Quick Start Guide

Get the Online Quiz App running in 5 minutes!

## Prerequisites Check

Before starting, make sure you have:
- ✅ Node.js installed (v14+): `node --version`
- ✅ MongoDB installed and running: `mongod --version`
- ✅ npm installed: `npm --version`

## Step-by-Step Setup

### 1️⃣ Start MongoDB

**Windows:**
```powershell
# Start MongoDB service
net start MongoDB
```

**Mac/Linux:**
```bash
sudo systemctl start mongod
# or
brew services start mongodb-community
```

### 2️⃣ Set Up Backend (Terminal 1)

```bash
# Navigate to backend
cd quiz-app/backend

# Install dependencies
npm install

# Seed the database with sample questions
npm run seed

# Start the server
npm run dev
```

✅ You should see: `Server is running on port 5000` and `MongoDB connected successfully`

### 3️⃣ Set Up Frontend (Terminal 2)

```bash
# Navigate to frontend (open new terminal)
cd quiz-app/frontend

# Install dependencies
npm install

# Start React app
npm start
```

✅ Your browser should automatically open to `http://localhost:3000`

## 🎉 That's It!

You should now see the Quiz App home page. Select a category and start quizzing!

## Common Issues

### MongoDB Not Running
```bash
# Check if MongoDB is running
# Windows
sc query MongoDB

# Mac/Linux
sudo systemctl status mongod
```

### Port 5000 Already in Use
Edit `backend/.env` and change:
```
PORT=5001
```

### Port 3000 Already in Use
```bash
# Set different port for React
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # Mac/Linux
```

## Testing the API

Open your browser or Postman:

```
GET http://localhost:5000/api/health
GET http://localhost:5000/api/questions
GET http://localhost:5000/api/questions/meta/categories
```

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🎨 Customize the questions in `backend/seedData.js`
- 🔧 Modify the UI in `frontend/src/components/`
- 🚀 Deploy your app to production

---

**Happy Quizzing! 🎯**
