# 🔄 Application Flow Diagram

## User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER OPENS APP                          │
│                    http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         HOME PAGE                               │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  🎯 Online Quiz App                                   │     │
│  │                                                        │     │
│  │  Select Category:                                     │     │
│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │     │
│  │  │📚  │ │🔬  │ │🔢  │ │📜  │ │🌍  │ │💻  │         │     │
│  │  │All │ │Sci │ │Math│ │Hist│ │Geo │ │Tech│         │     │
│  │  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘         │     │
│  │                                                        │     │
│  │  Quiz Rules:                                          │     │
│  │  • Answer all questions                               │     │
│  │  • Navigate freely                                    │     │
│  │  • Submit when ready                                  │     │
│  │                                                        │     │
│  │              [Start Quiz Button]                      │     │
│  └───────────────────────────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                             │ User clicks "Start Quiz"
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FETCH QUESTIONS (API Call)                   │
│  GET /api/questions?category=Science                            │
│  ← Backend returns questions (without correct answers)          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         QUIZ PAGE                               │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Quiz Time! 📝          Time: 0:45    Progress: 3/10  │     │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │     │
│  │  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]     │     │
│  │                                                        │     │
│  │  Question 3 of 10          [Science] [Medium]        │     │
│  │                                                        │     │
│  │  What is the powerhouse of the cell?                 │     │
│  │                                                        │     │
│  │  ┌─────────────────────────────────────────────┐     │     │
│  │  │ A  Nucleus                                   │     │     │
│  │  └─────────────────────────────────────────────┘     │     │
│  │  ┌─────────────────────────────────────────────┐     │     │
│  │  │ B  Ribosome                                  │     │     │
│  │  └─────────────────────────────────────────────┘     │     │
│  │  ┌─────────────────────────────────────────────┐     │     │
│  │  │ C  Mitochondria                          ✓   │ ◄── Selected
│  │  └─────────────────────────────────────────────┘     │     │
│  │  ┌─────────────────────────────────────────────┐     │     │
│  │  │ D  Endoplasmic Reticulum                     │     │     │
│  │  └─────────────────────────────────────────────┘     │     │
│  │                                                        │     │
│  │  [◄ Previous]                           [Next ►]     │     │
│  │                                                        │     │
│  │  Question Navigator:                                  │     │
│  │  ● ● ● ○ ○ ○ ○ ○ ○ ○                               │     │
│  │  (● = answered, ○ = unanswered)                      │     │
│  └───────────────────────────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                             │ User answers all questions
                             │ Clicks "Submit Quiz"
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SUBMIT ANSWERS (API Call)                     │
│  POST /api/questions/submit                                     │
│  Body: { answers: [                                             │
│    { questionId: "...", selectedAnswer: "Mitochondria" },      │
│    { questionId: "...", selectedAnswer: "Au" },                │
│    ...                                                          │
│  ]}                                                             │
│  ← Backend validates and returns score                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       RESULTS PAGE                              │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Quiz Results 📊                                      │     │
│  │                                                        │     │
│  │           ┌──────────────────┐                        │     │
│  │           │                  │                        │     │
│  │           │       80%        │                        │     │
│  │           │                  │                        │     │
│  │           │   Great Job! 🌟  │                        │     │
│  │           │                  │                        │     │
│  │           └──────────────────┘                        │     │
│  │                                                        │     │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │     │
│  │  │   ✅   │ │   ❌   │ │   📝   │ │   ⏱️   │        │     │
│  │  │   8    │ │   2    │ │   10   │ │  2:34  │        │     │
│  │  │Correct │ │Incorrect│ │ Total  │ │  Time  │        │     │
│  │  └────────┘ └────────┘ └────────┘ └────────┘        │     │
│  │                                                        │     │
│  │  Detailed Results:                                    │     │
│  │  ┌────────────────────────────────────────────┐      │     │
│  │  │ Question 1              ✓ Correct          │      │     │
│  │  │ What is the chemical symbol for gold?      │      │     │
│  │  │ Your Answer: Au ✓                          │      │     │
│  │  └────────────────────────────────────────────┘      │     │
│  │  ┌────────────────────────────────────────────┐      │     │
│  │  │ Question 2              ✗ Incorrect        │      │     │
│  │  │ What is the speed of light?                │      │     │
│  │  │ Your Answer: 150,000,000 m/s ✗             │      │     │
│  │  │ Correct Answer: 299,792,458 m/s            │      │     │
│  │  └────────────────────────────────────────────┘      │     │
│  │  ...                                                  │     │
│  │                                                        │     │
│  │  [Retake Quiz]         [Back to Home]                │     │
│  └───────────────────────────────────────────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
         [Retake Quiz]            [Back to Home]
                │                         │
                └────────────┬────────────┘
                             │
                             ▼
                    (Loop back to start)
```

## Technical Flow

### 1. Application Startup

```
MongoDB (Port 27017)
    ↓
Backend Server (Port 5000)
    ↓ connects to
MongoDB Database
    ↓
Express Routes Registered
    ↓
Server Listening
    ↓
Frontend (Port 3000)
    ↓ proxies API calls to
Backend Server
```

### 2. Data Flow - Fetch Questions

```
User clicks "Start Quiz"
    ↓
React Component (Quiz.js)
    ↓
axios.get('/api/questions?category=Science')
    ↓
Express Route Handler (questionRoutes.js)
    ↓
Mongoose Query (Question.find({ category: 'Science' }))
    ↓
MongoDB Database
    ↓
Returns Questions (without correctAnswer field)
    ↓
Express sends JSON response
    ↓
Axios receives data
    ↓
React setState updates
    ↓
Component re-renders with questions
```

### 3. Data Flow - Submit Answers

```
User clicks "Submit Quiz"
    ↓
React collects all answers
    ↓
axios.post('/api/questions/submit', { answers: [...] })
    ↓
Express Route Handler
    ↓
For each answer:
    ↓
    Mongoose Query (Question.findById)
    ↓
    Compare selectedAnswer with correctAnswer
    ↓
    Calculate isCorrect
    ↓
Calculate total score and percentage
    ↓
Express sends results JSON
    ↓
Axios receives results
    ↓
React Router navigates to /results
    ↓
Results component displays score
```

## State Management Flow

### Quiz Component State

```
Initial State:
├── questions: []
├── currentQuestionIndex: 0
├── answers: {}
├── loading: true
├── error: null
└── timeElapsed: 0

User Actions:
├── Select Answer → Update answers object
├── Next Button → Increment currentQuestionIndex
├── Previous Button → Decrement currentQuestionIndex
├── Click Dot → Set currentQuestionIndex
└── Submit → POST to API, navigate to results

Effects:
├── useEffect(() => fetchQuestions(), [])
└── useEffect(() => timer interval, [])
```

## Component Lifecycle

```
App Component Mounts
    ↓
React Router Initialized
    ↓
Route: "/" → Home Component
    ↓
Home Component Mounts
    ↓
useEffect: Fetch Categories
    ↓
User Selects Category
    ↓
User Clicks "Start Quiz"
    ↓
Navigate to "/quiz" with state
    ↓
Quiz Component Mounts
    ↓
useEffect: Fetch Questions
    ↓
useEffect: Start Timer
    ↓
User Interacts (answers questions)
    ↓
User Clicks "Submit"
    ↓
POST answers to API
    ↓
Navigate to "/results" with state
    ↓
Results Component Mounts
    ↓
Display results from location.state
    ↓
User Clicks "Retake" or "Home"
    ↓
Navigate accordingly
```

## API Request/Response Flow

### GET /api/questions

```
Request:
GET /api/questions?category=Science

Backend Processing:
1. Parse query parameters
2. Build filter object
3. Query database
4. Remove correctAnswer field
5. Send response

Response:
[
  {
    "_id": "...",
    "questionText": "What is the chemical symbol for gold?",
    "choices": ["Go", "Gd", "Au", "Ag"],
    "category": "Science",
    "difficulty": "Easy"
  },
  ...
]
```

### POST /api/questions/submit

```
Request:
POST /api/questions/submit
Body: {
  "answers": [
    {
      "questionId": "abc123",
      "selectedAnswer": "Au"
    }
  ]
}

Backend Processing:
1. Validate request body
2. For each answer:
   - Find question by ID
   - Compare with correct answer
   - Mark as correct/incorrect
3. Calculate statistics
4. Build results object
5. Send response

Response:
{
  "totalQuestions": 10,
  "correctAnswers": 8,
  "incorrectAnswers": 2,
  "percentage": 80.00,
  "results": [
    {
      "questionId": "abc123",
      "questionText": "What is the chemical symbol for gold?",
      "selectedAnswer": "Au",
      "correctAnswer": "Au",
      "isCorrect": true
    },
    ...
  ]
}
```

## Error Handling Flow

```
API Call
    ↓
Try Block
    ↓
Success? ──Yes──→ Process Data → Update State
    │
    No
    ↓
Catch Block
    ↓
Log Error
    ↓
Set Error State
    ↓
Display Error Message
    ↓
Provide Recovery Options
```

## Navigation Flow

```
Home (/)
    │
    ├─→ Start Quiz → Quiz (/quiz)
    │                    │
    │                    ├─→ Submit → Results (/results)
    │                    │               │
    │                    │               ├─→ Retake Quiz → Quiz (/quiz)
    │                    │               │
    │                    │               └─→ Back to Home → Home (/)
    │                    │
    │                    └─→ (User can't go back without submitting)
    │
    └─→ (Always accessible via browser back or manual navigation)
```

## Timer Flow

```
Quiz Component Mounts
    ↓
useEffect Hook Runs
    ↓
setInterval(() => {
    setTimeElapsed(prev => prev + 1)
}, 1000)
    ↓
Timer Updates Every Second
    ↓
Display: formatTime(timeElapsed)
    ↓
Component Unmounts
    ↓
clearInterval (cleanup)
```

## Responsive Design Flow

```
Screen Size Detection
    ↓
CSS Media Queries
    ↓
< 768px (Mobile)
    ├─→ Single column layout
    ├─→ Smaller fonts
    ├─→ Stacked navigation
    └─→ Touch-friendly buttons
    
768px - 1024px (Tablet)
    ├─→ Adjusted grid
    ├─→ Medium spacing
    └─→ Flexible layout
    
> 1024px (Desktop)
    ├─→ Multi-column layout
    ├─→ Larger fonts
    └─→ Optimal spacing
```

---

**This flow diagram shows the complete user journey and technical implementation!** 🎯
