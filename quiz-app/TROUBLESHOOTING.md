# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🗄️ MongoDB Issues

#### Issue: MongoDB Connection Failed
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```

**Solutions:**

1. **Check if MongoDB is running**
   ```powershell
   # Windows - Check service
   sc query MongoDB
   
   # Start MongoDB service
   net start MongoDB
   ```

2. **Verify MongoDB installation**
   ```bash
   mongod --version
   ```

3. **Check connection string in `.env`**
   ```
   MONGODB_URI=mongodb://localhost:27017/quizapp
   ```

4. **Try connecting manually**
   ```bash
   mongo
   # or
   mongosh
   ```

#### Issue: Database Seeding Failed
```
Error: Cannot seed database
```

**Solutions:**

1. **Ensure MongoDB is running first**
2. **Run seed command again**
   ```bash
   cd backend
   npm run seed
   ```

3. **Check for existing data**
   ```bash
   mongo quizapp
   db.questions.count()
   ```

---

### 🔌 Port Issues

#### Issue: Port 5000 Already in Use
```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solutions:**

1. **Change backend port**
   Edit `backend/.env`:
   ```
   PORT=5001
   ```

2. **Find and kill process using port 5000**
   ```powershell
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

3. **Use different port temporarily**
   ```bash
   set PORT=5001 && npm run dev
   ```

#### Issue: Port 3000 Already in Use
```
Something is already running on port 3000
```

**Solutions:**

1. **Use different port**
   ```powershell
   # Windows
   set PORT=3001 && npm start
   
   # Mac/Linux
   PORT=3001 npm start
   ```

2. **Kill process on port 3000**
   ```powershell
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   ```

---

### 📦 npm/Node Issues

#### Issue: npm install fails
```
Error: npm ERR! code EACCES
```

**Solutions:**

1. **Run as administrator** (Windows)
   - Right-click PowerShell
   - Select "Run as Administrator"

2. **Clear npm cache**
   ```bash
   npm cache clean --force
   npm install
   ```

3. **Delete node_modules and reinstall**
   ```bash
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

#### Issue: Module not found
```
Error: Cannot find module 'express'
```

**Solutions:**

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Check you're in correct directory**
   ```bash
   # For backend issues
   cd backend
   npm install
   
   # For frontend issues
   cd frontend
   npm install
   ```

---

### 🌐 CORS Issues

#### Issue: CORS Error in Browser
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solutions:**

1. **Verify CORS is enabled in backend**
   Check `server.js`:
   ```javascript
   app.use(cors());
   ```

2. **Check proxy in frontend**
   Verify `frontend/package.json`:
   ```json
   "proxy": "http://localhost:5000"
   ```

3. **Restart both servers**
   ```bash
   # Stop both servers (Ctrl+C)
   # Restart backend
   cd backend && npm run dev
   
   # Restart frontend
   cd frontend && npm start
   ```

---

### 🔄 API Issues

#### Issue: Cannot fetch questions
```
Error: Request failed with status code 500
```

**Solutions:**

1. **Check backend is running**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Verify database has questions**
   ```bash
   cd backend
   npm run seed
   ```

3. **Check backend console for errors**

4. **Test API directly**
   Open browser: `http://localhost:5000/api/questions`

#### Issue: Submit answers fails
```
Error: Invalid answers format
```

**Solutions:**

1. **Check answer format**
   Must be array of objects:
   ```json
   {
     "answers": [
       {
         "questionId": "...",
         "selectedAnswer": "..."
       }
     ]
   }
   ```

2. **Verify at least one answer is selected**

---

### ⚛️ React Issues

#### Issue: Blank page / White screen
```
Nothing appears in browser
```

**Solutions:**

1. **Check browser console for errors**
   - Press F12
   - Look at Console tab

2. **Verify frontend is running**
   ```bash
   cd frontend
   npm start
   ```

3. **Clear browser cache**
   - Ctrl+Shift+Delete
   - Clear cache and reload

4. **Check for JavaScript errors**

#### Issue: React Router not working
```
Cannot GET /quiz
```

**Solutions:**

1. **Use React development server**
   ```bash
   npm start
   ```

2. **Don't access files directly**
   Use `http://localhost:3000` not `file://`

3. **Check Router setup in App.js**

---

### 🎨 Styling Issues

#### Issue: Styles not loading
```
Page looks unstyled
```

**Solutions:**

1. **Check CSS imports**
   Verify imports in component files:
   ```javascript
   import './Home.css';
   ```

2. **Clear browser cache**

3. **Check CSS file paths**

4. **Restart development server**

---

### 💾 Data Issues

#### Issue: No questions available
```
No questions available for this category
```

**Solutions:**

1. **Seed the database**
   ```bash
   cd backend
   npm run seed
   ```

2. **Check MongoDB is running**

3. **Verify database connection**

#### Issue: Questions not filtering by category
```
All questions show regardless of category
```

**Solutions:**

1. **Check API call includes category**
   ```javascript
   axios.get('/api/questions', { params: { category } })
   ```

2. **Verify backend route handles category filter**

---

### 🖥️ Windows-Specific Issues

#### Issue: PowerShell script won't run
```
File cannot be loaded because running scripts is disabled
```

**Solutions:**

1. **Enable script execution**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Run individual commands manually**

#### Issue: MongoDB service not found
```
The specified service does not exist
```

**Solutions:**

1. **Install MongoDB as Windows service**
   During MongoDB installation, check "Install as Service"

2. **Run MongoDB manually**
   ```bash
   mongod --dbpath C:\data\db
   ```

---

### 🔍 Debugging Tips

#### Enable Verbose Logging

**Backend:**
```javascript
// Add to server.js
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});
```

**Frontend:**
```javascript
// Add to API calls
axios.get('/api/questions')
  .then(response => {
    console.log('Response:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

#### Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Reload page
4. Check API calls and responses

#### Verify Environment
```bash
# Check Node version
node --version

# Check npm version
npm --version

# Check MongoDB version
mongod --version

# List running processes
netstat -ano | findstr :5000
netstat -ano | findstr :3000
```

---

## 🆘 Still Having Issues?

### Checklist
- [ ] MongoDB is installed and running
- [ ] Node.js and npm are installed
- [ ] All dependencies are installed (`npm install`)
- [ ] Backend is running on port 5000
- [ ] Frontend is running on port 3000
- [ ] Database is seeded with questions
- [ ] No port conflicts
- [ ] Browser console shows no errors
- [ ] Network tab shows successful API calls

### Fresh Start
If all else fails, try a complete reset:

```bash
# 1. Stop all servers (Ctrl+C)

# 2. Clean backend
cd backend
rm -rf node_modules
rm package-lock.json
npm install
npm run seed

# 3. Clean frontend
cd ../frontend
rm -rf node_modules
rm package-lock.json
npm install

# 4. Restart MongoDB
net start MongoDB

# 5. Start backend
cd ../backend
npm run dev

# 6. Start frontend (new terminal)
cd ../frontend
npm start
```

---

## 📞 Getting Help

1. **Check Documentation**
   - README.md
   - QUICKSTART.md
   - PROJECT_OVERVIEW.md

2. **Review Code**
   - Check STRUCTURE.md for file locations
   - Look at console logs
   - Use browser DevTools

3. **Common Patterns**
   - Most issues are port conflicts or MongoDB not running
   - Always check both backend and frontend consoles
   - Verify environment variables

---

**Most issues can be solved by ensuring MongoDB is running and ports are available!** 🎯
