import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/api/questions/meta/categories');
      setCategories(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setLoading(false);
    }
  };

  const startQuiz = () => {
    navigate('/quiz', { state: { category: selectedCategory } });
  };

  return (
    <div className="container home-container">
      <h1>🎯 Online Quiz App</h1>
      <div className="home-content">
        <p className="welcome-text">
          Test your knowledge across various categories! Select a category below and start your quiz.
        </p>
        
        <div className="category-section">
          <h2>Select Category</h2>
          {loading ? (
            <p>Loading categories...</p>
          ) : (
            <div className="category-grid">
              <div
                className={`category-card ${selectedCategory === 'all' ? 'selected' : ''}`}
                onClick={() => setSelectedCategory('all')}
              >
                <span className="category-icon">📚</span>
                <span className="category-name">All Categories</span>
              </div>
              {categories.map((category) => (
                <div
                  key={category}
                  className={`category-card ${selectedCategory === category ? 'selected' : ''}`}
                  onClick={() => setSelectedCategory(category)}
                >
                  <span className="category-icon">
                    {category === 'Science' && '🔬'}
                    {category === 'Math' && '🔢'}
                    {category === 'History' && '📜'}
                    {category === 'Geography' && '🌍'}
                    {category === 'Technology' && '💻'}
                  </span>
                  <span className="category-name">{category}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="quiz-info">
          <h3>Quiz Rules:</h3>
          <ul>
            <li>Answer all questions to the best of your ability</li>
            <li>You can navigate between questions</li>
            <li>Submit when you're ready to see your score</li>
            <li>Review correct answers after submission</li>
          </ul>
        </div>

        <button className="btn btn-start" onClick={startQuiz}>
          Start Quiz
        </button>
      </div>
    </div>
  );
}

export default Home;
