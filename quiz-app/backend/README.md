# Backend API Documentation

## Overview

RESTful API built with Express.js and MongoDB for the Quiz Application.

## Setup

```bash
npm install
npm run seed    # Seed database
npm run dev     # Development mode
npm start       # Production mode
```

## Environment Variables

Create a `.env` file:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/quizapp
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server status.

### Get All Questions
```
GET /api/questions
Query Params:
  - category (optional): Filter by category
  - difficulty (optional): Filter by difficulty level
```

### Get Single Question
```
GET /api/questions/:id
```

### Submit Quiz Answers
```
POST /api/questions/submit
Body: {
  "answers": [
    {
      "questionId": "string",
      "selectedAnswer": "string"
    }
  ]
}
```

### Get Categories
```
GET /api/questions/meta/categories
```

## Database Schema

```javascript
Question {
  questionText: String,
  choices: [String],
  correctAnswer: String,
  category: String,
  difficulty: String,
  timestamps: Date
}
```

## Adding New Questions

Edit `seedData.js` and run:
```bash
npm run seed
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Server Error
