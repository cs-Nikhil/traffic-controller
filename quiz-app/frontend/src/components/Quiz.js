import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import './Quiz.css';

function Quiz() {
  const navigate = useNavigate();
  const location = useLocation();
  const category = location.state?.category || 'all';

  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeElapsed, setTimeElapsed] = useState(0);

  useEffect(() => {
    fetchQuestions();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const fetchQuestions = async () => {
    try {
      const params = category !== 'all' ? { category } : {};
      const response = await axios.get('/api/questions', { params });
      
      if (response.data.length === 0) {
        setError('No questions available for this category.');
        setLoading(false);
        return;
      }
      
      setQuestions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
      setError('Failed to load questions. Please try again.');
      setLoading(false);
    }
  };

  const handleAnswerSelect = (answer) => {
    setAnswers({
      ...answers,
      [questions[currentQuestionIndex]._id]: answer
    });
  };

  const goToNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const goToPreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = async () => {
    const answersArray = questions.map((question) => ({
      questionId: question._id,
      selectedAnswer: answers[question._id] || ''
    }));

    try {
      const response = await axios.post('/api/questions/submit', {
        answers: answersArray
      });

      navigate('/results', {
        state: {
          results: response.data,
          timeElapsed,
          category
        }
      });
    } catch (error) {
      console.error('Error submitting answers:', error);
      alert('Failed to submit answers. Please try again.');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getAnsweredCount = () => {
    return Object.keys(answers).length;
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading questions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
        <button className="btn" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const selectedAnswer = answers[currentQuestion._id];

  return (
    <div className="container quiz-container">
      <div className="quiz-header">
        <h1>Quiz Time! 📝</h1>
        <div className="quiz-stats">
          <div className="stat">
            <span className="stat-label">Time:</span>
            <span className="stat-value">{formatTime(timeElapsed)}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Progress:</span>
            <span className="stat-value">
              {getAnsweredCount()} / {questions.length}
            </span>
          </div>
        </div>
      </div>

      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
        ></div>
      </div>

      <div className="question-card">
        <div className="question-header">
          <span className="question-number">
            Question {currentQuestionIndex + 1} of {questions.length}
          </span>
          <div className="question-meta">
            <span className="badge">{currentQuestion.category}</span>
            <span className="badge badge-difficulty">{currentQuestion.difficulty}</span>
          </div>
        </div>

        <h2 className="question-text">{currentQuestion.questionText}</h2>

        <div className="choices">
          {currentQuestion.choices.map((choice, index) => (
            <div
              key={index}
              className={`choice ${selectedAnswer === choice ? 'selected' : ''}`}
              onClick={() => handleAnswerSelect(choice)}
            >
              <span className="choice-letter">{String.fromCharCode(65 + index)}</span>
              <span className="choice-text">{choice}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="navigation-buttons">
        <button
          className="btn btn-secondary"
          onClick={goToPreviousQuestion}
          disabled={currentQuestionIndex === 0}
        >
          ← Previous
        </button>

        {currentQuestionIndex === questions.length - 1 ? (
          <button
            className="btn btn-submit"
            onClick={handleSubmit}
            disabled={getAnsweredCount() === 0}
          >
            Submit Quiz
          </button>
        ) : (
          <button className="btn" onClick={goToNextQuestion}>
            Next →
          </button>
        )}
      </div>

      <div className="question-navigator">
        {questions.map((_, index) => (
          <div
            key={index}
            className={`nav-dot ${index === currentQuestionIndex ? 'active' : ''} ${
              answers[questions[index]._id] ? 'answered' : ''
            }`}
            onClick={() => setCurrentQuestionIndex(index)}
            title={`Question ${index + 1}`}
          ></div>
        ))}
      </div>
    </div>
  );
}

export default Quiz;
