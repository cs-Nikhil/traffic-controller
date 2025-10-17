# 📂 Project Structure

## Complete File Tree

```
quiz-app/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick setup guide
├── 📄 PROJECT_OVERVIEW.md          # Detailed project overview
├── 📄 STRUCTURE.md                 # This file
├── 🔧 setup.ps1                    # Setup automation script
├── 🚀 start-app.ps1                # Start app script
│
├── 📁 backend/                     # Backend API
│   ├── 📁 config/
│   │   └── database.js             # MongoDB connection config
│   │
│   ├── 📁 models/
│   │   └── Question.js             # Question schema/model
│   │
│   ├── 📁 routes/
│   │   └── questionRoutes.js       # API route handlers
│   │
│   ├── 📄 .env                     # Environment variables
│   ├── 📄 .gitignore               # Git ignore rules
│   ├── 📄 package.json             # Backend dependencies
│   ├── 📄 README.md                # Backend documentation
│   ├── 📄 seedData.js              # Database seeding script
│   └── 📄 server.js                # Express server entry point
│
└── 📁 frontend/                    # React frontend
    ├── 📁 public/
    │   └── index.html              # HTML template
    │
    ├── 📁 src/
    │   ├── 📁 components/
    │   │   ├── Home.js             # Home page component
    │   │   ├── Home.css            # Home page styles
    │   │   ├── Quiz.js             # Quiz interface component
    │   │   ├── Quiz.css            # Quiz interface styles
    │   │   ├── Results.js          # Results page component
    │   │   └── Results.css         # Results page styles
    │   │
    │   ├── App.js                  # Main app component
    │   ├── App.css                 # Main app styles
    │   ├── index.js                # React entry point
    │   └── index.css               # Global styles
    │
    ├── 📄 .gitignore               # Git ignore rules
    ├── 📄 package.json             # Frontend dependencies
    └── 📄 README.md                # Frontend documentation
```

## 📋 File Descriptions

### Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation with setup instructions |
| `QUICKSTART.md` | 5-minute quick start guide |
| `PROJECT_OVERVIEW.md` | Detailed overview of features and architecture |
| `STRUCTURE.md` | This file - project structure guide |
| `setup.ps1` | PowerShell script to automate setup |
| `start-app.ps1` | PowerShell script to start both servers |

### Backend Files

#### Configuration
- **`config/database.js`**: MongoDB connection logic using Mongoose

#### Models
- **`models/Question.js`**: Mongoose schema for quiz questions
  - Fields: questionText, choices, correctAnswer, category, difficulty

#### Routes
- **`routes/questionRoutes.js`**: All API endpoints
  - GET `/api/questions` - Fetch questions
  - GET `/api/questions/:id` - Fetch single question
  - POST `/api/questions/submit` - Submit answers
  - GET `/api/questions/meta/categories` - Get categories

#### Core Files
- **`server.js`**: Express server setup, middleware, and startup
- **`seedData.js`**: Script to populate database with 25 sample questions
- **`.env`**: Environment variables (PORT, MONGODB_URI)
- **`package.json`**: Dependencies and npm scripts

### Frontend Files

#### Components
- **`Home.js`**: Landing page with category selection
- **`Quiz.js`**: Main quiz interface with questions and navigation
- **`Results.js`**: Results display with score and review

#### Styles
- **`Home.css`**: Styles for home page (category cards, grid layout)
- **`Quiz.css`**: Styles for quiz interface (questions, choices, progress)
- **`Results.css`**: Styles for results page (score circle, statistics)
- **`App.css`**: Global app styles (buttons, containers, animations)
- **`index.css`**: Base styles (body, fonts, background)

#### Core Files
- **`App.js`**: Main component with React Router setup
- **`index.js`**: React DOM rendering entry point
- **`package.json`**: Dependencies and build scripts

## 🔄 Data Flow

```
User Action → React Component → Axios Request → Express Route → 
Mongoose Model → MongoDB → Response → React State → UI Update
```

## 📦 Key Dependencies

### Backend
```
express         → Web framework
mongoose        → MongoDB ODM
cors            → Cross-origin resource sharing
dotenv          → Environment variables
nodemon         → Auto-restart server (dev)
```

### Frontend
```
react           → UI library
react-dom       → React rendering
react-router-dom → Routing
axios           → HTTP client
react-scripts   → Build tools
```

## 🎯 Component Hierarchy

```
App (Router)
├── Home
│   └── Category Selection
│       └── Start Button
│
├── Quiz
│   ├── Quiz Header (Timer, Progress)
│   ├── Question Card
│   │   ├── Question Text
│   │   └── Choices (A, B, C, D)
│   ├── Navigation Buttons
│   └── Question Navigator Dots
│
└── Results
    ├── Score Summary
    │   ├── Score Circle
    │   └── Statistics Grid
    ├── Detailed Results List
    │   └── Question Review Items
    └── Action Buttons
```

## 🔐 Environment Variables

### Backend `.env`
```
PORT=5000
MONGODB_URI=mongodb://localhost:27017/quizapp
```

### Frontend (via proxy)
```
Configured in package.json:
"proxy": "http://localhost:5000"
```

## 📊 Database Collections

### Questions Collection
```
quizapp
└── questions (collection)
    ├── Document 1 (Science question)
    ├── Document 2 (Math question)
    ├── Document 3 (History question)
    └── ... (25 total documents)
```

## 🚀 Startup Sequence

1. **MongoDB** starts (port 27017)
2. **Backend** starts (port 5000)
   - Connects to MongoDB
   - Registers routes
   - Listens for requests
3. **Frontend** starts (port 3000)
   - Proxies API calls to backend
   - Renders React app
   - Opens browser

## 📝 Notes

- All backend routes are prefixed with `/api`
- Frontend uses proxy to avoid CORS issues in development
- Database is seeded with sample data on first run
- Responsive design works on mobile, tablet, and desktop
- No authentication required (can be added as enhancement)

## 🎨 Styling Architecture

```
Global Styles (index.css)
    ↓
App Styles (App.css)
    ↓
Component Styles (Home.css, Quiz.css, Results.css)
```

## 🔧 Build & Deploy

### Development
```bash
Backend:  npm run dev (nodemon)
Frontend: npm start (webpack-dev-server)
```

### Production
```bash
Backend:  npm start (node)
Frontend: npm run build (optimized build)
```

---

**Navigate the codebase with confidence! 🗺️**
