const express = require('express');
const router = express.Router();
const Question = require('../models/Question');

// GET /api/questions - Fetch all quiz questions
router.get('/', async (req, res) => {
  try {
    const { category, difficulty } = req.query;
    let filter = {};
    
    if (category) filter.category = category;
    if (difficulty) filter.difficulty = difficulty;
    
    const questions = await Question.find(filter).select('-__v');
    
    // Return questions without revealing correct answers
    const questionsForQuiz = questions.map(q => ({
      _id: q._id,
      questionText: q.questionText,
      choices: q.choices,
      category: q.category,
      difficulty: q.difficulty
    }));
    
    res.json(questionsForQuiz);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching questions', error: error.message });
  }
});

// GET /api/questions/:id - Fetch a single question
router.get('/:id', async (req, res) => {
  try {
    const question = await Question.findById(req.params.id).select('-correctAnswer -__v');
    
    if (!question) {
      return res.status(404).json({ message: 'Question not found' });
    }
    
    res.json(question);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching question', error: error.message });
  }
});

// POST /api/questions/submit - Submit answers and get score
router.post('/submit', async (req, res) => {
  try {
    const { answers } = req.body; // answers: [{ questionId, selectedAnswer }]
    
    if (!answers || !Array.isArray(answers)) {
      return res.status(400).json({ message: 'Invalid answers format' });
    }
    
    let correctCount = 0;
    const results = [];
    
    for (const answer of answers) {
      const question = await Question.findById(answer.questionId);
      
      if (question) {
        const isCorrect = question.correctAnswer === answer.selectedAnswer;
        if (isCorrect) correctCount++;
        
        results.push({
          questionId: question._id,
          questionText: question.questionText,
          selectedAnswer: answer.selectedAnswer,
          correctAnswer: question.correctAnswer,
          isCorrect
        });
      }
    }
    
    const totalQuestions = answers.length;
    const percentage = totalQuestions > 0 ? ((correctCount / totalQuestions) * 100).toFixed(2) : 0;
    
    res.json({
      totalQuestions,
      correctAnswers: correctCount,
      incorrectAnswers: totalQuestions - correctCount,
      percentage: parseFloat(percentage),
      results
    });
  } catch (error) {
    res.status(500).json({ message: 'Error submitting answers', error: error.message });
  }
});

// GET /api/questions/categories - Get all categories
router.get('/meta/categories', async (req, res) => {
  try {
    const categories = await Question.distinct('category');
    res.json(categories);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching categories', error: error.message });
  }
});

module.exports = router;
