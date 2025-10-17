const mongoose = require('mongoose');
const dotenv = require('dotenv');
const Question = require('./models/Question');

dotenv.config();

const sampleQuestions = [
  // Science Questions
  {
    questionText: "What is the chemical symbol for gold?",
    choices: ["Go", "Gd", "Au", "Ag"],
    correctAnswer: "Au",
    category: "Science",
    difficulty: "Easy"
  },
  {
    questionText: "What is the speed of light in vacuum?",
    choices: ["299,792,458 m/s", "150,000,000 m/s", "500,000,000 m/s", "100,000,000 m/s"],
    correctAnswer: "299,792,458 m/s",
    category: "Science",
    difficulty: "Medium"
  },
  {
    questionText: "What is the powerhouse of the cell?",
    choices: ["Nucleus", "Ribosome", "Mitochondria", "Endoplasmic Reticulum"],
    correctAnswer: "Mitochondria",
    category: "Science",
    difficulty: "Easy"
  },
  {
    questionText: "What is the atomic number of Carbon?",
    choices: ["6", "12", "8", "14"],
    correctAnswer: "6",
    category: "Science",
    difficulty: "Medium"
  },
  {
    questionText: "Which planet is known as the Red Planet?",
    choices: ["Venus", "Mars", "Jupiter", "Saturn"],
    correctAnswer: "Mars",
    category: "Science",
    difficulty: "Easy"
  },
  
  // Math Questions
  {
    questionText: "What is the value of π (pi) approximately?",
    choices: ["3.14159", "2.71828", "1.61803", "4.66920"],
    correctAnswer: "3.14159",
    category: "Math",
    difficulty: "Easy"
  },
  {
    questionText: "What is the square root of 144?",
    choices: ["10", "11", "12", "13"],
    correctAnswer: "12",
    category: "Math",
    difficulty: "Easy"
  },
  {
    questionText: "What is the derivative of x²?",
    choices: ["x", "2x", "x²", "2x²"],
    correctAnswer: "2x",
    category: "Math",
    difficulty: "Medium"
  },
  {
    questionText: "What is 15% of 200?",
    choices: ["25", "30", "35", "40"],
    correctAnswer: "30",
    category: "Math",
    difficulty: "Easy"
  },
  {
    questionText: "What is the sum of angles in a triangle?",
    choices: ["90 degrees", "180 degrees", "270 degrees", "360 degrees"],
    correctAnswer: "180 degrees",
    category: "Math",
    difficulty: "Easy"
  },
  
  // History Questions
  {
    questionText: "In which year did World War II end?",
    choices: ["1943", "1944", "1945", "1946"],
    correctAnswer: "1945",
    category: "History",
    difficulty: "Medium"
  },
  {
    questionText: "Who was the first President of the United States?",
    choices: ["Thomas Jefferson", "George Washington", "John Adams", "Benjamin Franklin"],
    correctAnswer: "George Washington",
    category: "History",
    difficulty: "Easy"
  },
  {
    questionText: "Which ancient wonder is still standing today?",
    choices: ["Hanging Gardens of Babylon", "Colossus of Rhodes", "Great Pyramid of Giza", "Lighthouse of Alexandria"],
    correctAnswer: "Great Pyramid of Giza",
    category: "History",
    difficulty: "Medium"
  },
  {
    questionText: "Who painted the Mona Lisa?",
    choices: ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
    correctAnswer: "Leonardo da Vinci",
    category: "History",
    difficulty: "Easy"
  },
  {
    questionText: "In which year did the Titanic sink?",
    choices: ["1910", "1911", "1912", "1913"],
    correctAnswer: "1912",
    category: "History",
    difficulty: "Medium"
  },
  
  // Geography Questions
  {
    questionText: "What is the capital of France?",
    choices: ["London", "Berlin", "Paris", "Madrid"],
    correctAnswer: "Paris",
    category: "Geography",
    difficulty: "Easy"
  },
  {
    questionText: "Which is the largest ocean on Earth?",
    choices: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
    correctAnswer: "Pacific Ocean",
    category: "Geography",
    difficulty: "Easy"
  },
  {
    questionText: "What is the longest river in the world?",
    choices: ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"],
    correctAnswer: "Nile River",
    category: "Geography",
    difficulty: "Medium"
  },
  {
    questionText: "How many continents are there?",
    choices: ["5", "6", "7", "8"],
    correctAnswer: "7",
    category: "Geography",
    difficulty: "Easy"
  },
  {
    questionText: "What is the smallest country in the world?",
    choices: ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
    correctAnswer: "Vatican City",
    category: "Geography",
    difficulty: "Medium"
  },
  
  // Technology Questions
  {
    questionText: "What does HTML stand for?",
    choices: ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"],
    correctAnswer: "Hyper Text Markup Language",
    category: "Technology",
    difficulty: "Easy"
  },
  {
    questionText: "Who is known as the father of computers?",
    choices: ["Alan Turing", "Charles Babbage", "Bill Gates", "Steve Jobs"],
    correctAnswer: "Charles Babbage",
    category: "Technology",
    difficulty: "Medium"
  },
  {
    questionText: "What does CPU stand for?",
    choices: ["Central Processing Unit", "Computer Personal Unit", "Central Processor Utility", "Computer Processing Unit"],
    correctAnswer: "Central Processing Unit",
    category: "Technology",
    difficulty: "Easy"
  },
  {
    questionText: "Which programming language is known as the 'language of the web'?",
    choices: ["Python", "Java", "JavaScript", "C++"],
    correctAnswer: "JavaScript",
    category: "Technology",
    difficulty: "Easy"
  },
  {
    questionText: "What year was the first iPhone released?",
    choices: ["2005", "2006", "2007", "2008"],
    correctAnswer: "2007",
    category: "Technology",
    difficulty: "Medium"
  }
];

const seedDatabase = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    
    console.log('Connected to MongoDB');
    
    // Clear existing questions
    await Question.deleteMany({});
    console.log('Cleared existing questions');
    
    // Insert sample questions
    await Question.insertMany(sampleQuestions);
    console.log(`Successfully seeded ${sampleQuestions.length} questions`);
    
    process.exit(0);
  } catch (error) {
    console.error('Error seeding database:', error);
    process.exit(1);
  }
};

seedDatabase();
