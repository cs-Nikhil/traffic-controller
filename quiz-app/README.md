# 🎯 Online Quiz Application

A full-stack web application for taking interactive quizzes with real-time scoring and detailed results analysis.

## 📋 Features

- **Multiple Categories**: Science, Math, History, Geography, Technology
- **Interactive Quiz Interface**: Clean, modern UI with smooth transitions
- **Real-time Timer**: Track time spent on each quiz
- **Progress Tracking**: Visual indicators for answered questions
- **Instant Results**: Detailed score breakdown with correct/incorrect answers
- **Question Navigation**: Move between questions freely
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Difficulty Levels**: Questions categorized by Easy, Medium, and Hard

## 🛠️ Technologies Used

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM for MongoDB
- **CORS** - Cross-origin resource sharing
- **dotenv** - Environment variable management

### Frontend
- **React** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **CSS3** - Styling with modern features

## 📁 Project Structure

```
quiz-app/
├── backend/
│   ├── config/
│   │   └── database.js          # MongoDB connection
│   ├── models/
│   │   └── Question.js          # Question schema
│   ├── routes/
│   │   └── questionRoutes.js    # API routes
│   ├── .env                     # Environment variables
│   ├── .gitignore
│   ├── package.json
│   ├── seedData.js              # Database seeding script
│   └── server.js                # Express server
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── Home.js          # Landing page
    │   │   ├── Home.css
    │   │   ├── Quiz.js          # Quiz interface
    │   │   ├── Quiz.css
    │   │   ├── Results.js       # Results page
    │   │   └── Results.css
    │   ├── App.js               # Main app component
    │   ├── App.css
    │   ├── index.js             # Entry point
    │   └── index.css
    ├── .gitignore
    └── package.json
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- MongoDB (v4.4 or higher)
- npm or yarn

### Installation

#### 1. Clone or navigate to the project directory

```bash
cd quiz-app
```

#### 2. Set up the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create .env file (already created, but verify the content)
# Make sure MongoDB URI is correct in .env file

# Start MongoDB (if not already running)
# On Windows: Start MongoDB service from Services
# On Mac/Linux: sudo systemctl start mongod

# Seed the database with sample questions
npm run seed

# Start the backend server
npm run dev
```

The backend server will start on `http://localhost:5000`

#### 3. Set up the Frontend

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will start on `http://localhost:3000`

## 🔌 API Endpoints

### GET /api/questions
Fetch all quiz questions (without correct answers)

**Query Parameters:**
- `category` (optional): Filter by category
- `difficulty` (optional): Filter by difficulty

**Response:**
```json
[
  {
    "_id": "...",
    "questionText": "What is the chemical symbol for gold?",
    "choices": ["Go", "Gd", "Au", "Ag"],
    "category": "Science",
    "difficulty": "Easy"
  }
]
```

### GET /api/questions/:id
Fetch a single question by ID (without correct answer)

### POST /api/questions/submit
Submit quiz answers and get score

**Request Body:**
```json
{
  "answers": [
    {
      "questionId": "...",
      "selectedAnswer": "Au"
    }
  ]
}
```

**Response:**
```json
{
  "totalQuestions": 10,
  "correctAnswers": 8,
  "incorrectAnswers": 2,
  "percentage": 80.00,
  "results": [
    {
      "questionId": "...",
      "questionText": "...",
      "selectedAnswer": "Au",
      "correctAnswer": "Au",
      "isCorrect": true
    }
  ]
}
```

### GET /api/questions/meta/categories
Get all available categories

### GET /api/health
Health check endpoint

## 💡 Usage

1. **Start the Application**: Follow the installation steps above
2. **Select Category**: Choose a quiz category from the home page
3. **Take the Quiz**: Answer questions at your own pace
4. **Navigate**: Use Previous/Next buttons or click on question dots
5. **Submit**: Click "Submit Quiz" when ready
6. **View Results**: See your score and review correct answers

## 🎨 Features in Detail

### Home Page
- Category selection with visual cards
- Quiz rules and instructions
- Responsive grid layout

### Quiz Interface
- One question at a time display
- Multiple choice options (A, B, C, D)
- Real-time timer
- Progress bar
- Question navigator dots
- Answer tracking

### Results Page
- Score percentage with color-coded feedback
- Statistics: Correct, Incorrect, Total, Time
- Detailed question-by-question review
- Correct answer revelation
- Option to retake quiz

## 🔧 Configuration

### Backend Configuration (.env)
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/quizapp
```

### Frontend Configuration
The frontend is configured to proxy API requests to `http://localhost:5000` (see `package.json`)

## 📊 Database Schema

### Question Model
```javascript
{
  questionText: String (required),
  choices: [String] (required),
  correctAnswer: String (required),
  category: String (default: 'General'),
  difficulty: String (enum: ['Easy', 'Medium', 'Hard']),
  timestamps: true
}
```

## 🧪 Sample Data

The application comes with 25 pre-loaded questions across 5 categories:
- Science (5 questions)
- Math (5 questions)
- History (5 questions)
- Geography (5 questions)
- Technology (5 questions)

## 🚀 Deployment

### Backend Deployment
1. Set up MongoDB Atlas or another cloud MongoDB service
2. Update `MONGODB_URI` in production environment
3. Deploy to Heroku, AWS, or any Node.js hosting service

### Frontend Deployment
1. Update API endpoint in frontend (remove proxy, use full URL)
2. Build the production version: `npm run build`
3. Deploy to Netlify, Vercel, or any static hosting service

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a full-stack learning project demonstrating:
- RESTful API design
- React component architecture
- State management
- Responsive design
- Database operations
- Full-stack integration

## 🐛 Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check the connection string in `.env`
- Verify MongoDB port (default: 27017)

### Port Already in Use
- Backend: Change `PORT` in `.env`
- Frontend: Set `PORT=3001` before running `npm start`

### CORS Issues
- Ensure backend CORS is properly configured
- Check proxy setting in frontend `package.json`

## 📞 Support

For issues or questions, please create an issue in the project repository.

---

**Enjoy the Quiz! 🎉**
