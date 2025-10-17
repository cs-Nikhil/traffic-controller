# 🎯 Get Started with Quiz App

## 🚀 Three Ways to Start

### Option 1: Automated Setup (Recommended for Windows)
```powershell
# Run setup script (one time only)
cd quiz-app
.\setup.ps1

# Start the app (every time)
.\start-app.ps1
```

### Option 2: Manual Setup
```bash
# Terminal 1 - Backend
cd quiz-app/backend
npm install
npm run seed
npm run dev

# Terminal 2 - Frontend  
cd quiz-app/frontend
npm install
npm start
```

### Option 3: Step-by-Step
Follow the detailed guide in [QUICKSTART.md](QUICKSTART.md)

## ✅ Prerequisites

Before starting, ensure you have:

1. **Node.js** (v14 or higher)
   ```bash
   node --version
   ```

2. **MongoDB** (v4.4 or higher)
   ```bash
   mongod --version
   ```

3. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

## 📚 Documentation Guide

| Document | When to Read |
|----------|--------------|
| **GET_STARTED.md** | 👈 You are here! Start here |
| **QUICKSTART.md** | Quick 5-minute setup |
| **README.md** | Complete documentation |
| **PROJECT_OVERVIEW.md** | Understand the project |
| **STRUCTURE.md** | Navigate the codebase |
| **backend/README.md** | Backend API details |
| **frontend/README.md** | Frontend component details |

## 🎯 First Time Setup Checklist

- [ ] Install Node.js
- [ ] Install MongoDB
- [ ] Clone/download project
- [ ] Navigate to `quiz-app` directory
- [ ] Run setup script OR manual setup
- [ ] Verify MongoDB is running
- [ ] Start backend server (port 5000)
- [ ] Start frontend server (port 3000)
- [ ] Open browser to http://localhost:3000
- [ ] Select a category and start quiz!

## 🔍 Quick Test

After starting the app, test these URLs:

1. **Frontend**: http://localhost:3000
2. **Backend Health**: http://localhost:5000/api/health
3. **Get Questions**: http://localhost:5000/api/questions

## 🎮 How to Use the App

1. **Home Page**
   - Select a quiz category (or "All Categories")
   - Click "Start Quiz"

2. **Quiz Page**
   - Read each question
   - Select an answer (A, B, C, or D)
   - Use "Next" to move forward
   - Use "Previous" to go back
   - Click dots to jump to specific questions
   - Click "Submit Quiz" when done

3. **Results Page**
   - View your score percentage
   - See statistics (correct/incorrect/total/time)
   - Review each question with correct answers
   - Click "Retake Quiz" or "Back to Home"

## 🎨 Features to Try

- ✅ Take a quiz in different categories
- ✅ Navigate between questions
- ✅ Skip questions and come back
- ✅ Watch the timer count up
- ✅ See progress bar update
- ✅ Review correct answers after submission
- ✅ Try on mobile device (responsive design)

## 🛠️ Customization Ideas

### Easy Customizations
1. **Add More Questions**: Edit `backend/seedData.js`
2. **Change Colors**: Edit CSS files in `frontend/src/components/`
3. **Modify Categories**: Update question categories and icons

### Advanced Customizations
1. Add user authentication
2. Create admin panel
3. Add timer countdown
4. Implement difficulty levels
5. Add leaderboard

## 🐛 Troubleshooting

### Problem: MongoDB won't start
**Solution**: 
```powershell
# Windows
net start MongoDB

# Or install MongoDB as a service
```

### Problem: Port 5000 is in use
**Solution**: Edit `backend/.env`
```
PORT=5001
```

### Problem: Port 3000 is in use
**Solution**: 
```bash
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # Mac/Linux
```

### Problem: Cannot connect to backend
**Solution**: 
- Check backend is running on port 5000
- Verify proxy in `frontend/package.json`
- Check CORS is enabled in backend

## 📞 Need Help?

1. Check [README.md](README.md) for detailed docs
2. Review [QUICKSTART.md](QUICKSTART.md) for setup
3. See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture
4. Check [STRUCTURE.md](STRUCTURE.md) for file locations

## 🎓 Learning Path

### Beginner
1. Run the app and take a quiz
2. Read README.md
3. Explore the code structure
4. Modify some questions in seedData.js

### Intermediate
1. Add new API endpoints
2. Create new React components
3. Modify the UI/styling
4. Add new features

### Advanced
1. Add authentication
2. Create admin dashboard
3. Implement real-time features
4. Deploy to production

## 🚀 Next Steps

After getting the app running:

1. ✅ Take a quiz to see all features
2. 📖 Read the full documentation
3. 🔧 Try customizing questions or styles
4. 🎨 Experiment with the code
5. 🚀 Add your own features

## 🎉 You're Ready!

The quiz app is now set up and ready to use. Have fun testing your knowledge!

---

**Questions? Check the documentation files or explore the code!**

Happy Quizzing! 🎯
