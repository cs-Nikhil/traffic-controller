import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Results.css';

function Results() {
  const navigate = useNavigate();
  const location = useLocation();
  const { results, timeElapsed, category } = location.state || {};

  if (!results) {
    return (
      <div className="container">
        <div className="error">No results available</div>
        <button className="btn" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    );
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getScoreMessage = (percentage) => {
    if (percentage >= 90) return { text: 'Outstanding! 🏆', color: '#28a745' };
    if (percentage >= 75) return { text: 'Great Job! 🌟', color: '#17a2b8' };
    if (percentage >= 60) return { text: 'Good Effort! 👍', color: '#ffc107' };
    if (percentage >= 40) return { text: 'Keep Practicing! 📚', color: '#fd7e14' };
    return { text: 'Need More Practice! 💪', color: '#dc3545' };
  };

  const scoreMessage = getScoreMessage(results.percentage);

  return (
    <div className="container results-container">
      <h1>Quiz Results 📊</h1>

      <div className="score-summary">
        <div className="score-circle" style={{ borderColor: scoreMessage.color }}>
          <div className="score-percentage" style={{ color: scoreMessage.color }}>
            {results.percentage}%
          </div>
          <div className="score-message" style={{ color: scoreMessage.color }}>
            {scoreMessage.text}
          </div>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-number">{results.correctAnswers}</div>
            <div className="stat-label">Correct</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">❌</div>
            <div className="stat-number">{results.incorrectAnswers}</div>
            <div className="stat-label">Incorrect</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📝</div>
            <div className="stat-number">{results.totalQuestions}</div>
            <div className="stat-label">Total</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-number">{formatTime(timeElapsed)}</div>
            <div className="stat-label">Time</div>
          </div>
        </div>
      </div>

      <div className="results-details">
        <h2>Detailed Results</h2>
        <div className="results-list">
          {results.results.map((result, index) => (
            <div
              key={result.questionId}
              className={`result-item ${result.isCorrect ? 'correct' : 'incorrect'}`}
            >
              <div className="result-header">
                <span className="result-number">Question {index + 1}</span>
                <span className={`result-badge ${result.isCorrect ? 'badge-correct' : 'badge-incorrect'}`}>
                  {result.isCorrect ? '✓ Correct' : '✗ Incorrect'}
                </span>
              </div>
              <div className="result-question">{result.questionText}</div>
              <div className="result-answers">
                <div className="answer-row">
                  <span className="answer-label">Your Answer:</span>
                  <span className={`answer-value ${result.isCorrect ? 'correct-answer' : 'wrong-answer'}`}>
                    {result.selectedAnswer || 'Not answered'}
                  </span>
                </div>
                {!result.isCorrect && (
                  <div className="answer-row">
                    <span className="answer-label">Correct Answer:</span>
                    <span className="answer-value correct-answer">
                      {result.correctAnswer}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="action-buttons">
        <button className="btn" onClick={() => navigate('/quiz', { state: { category } })}>
          Retake Quiz
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Results;
