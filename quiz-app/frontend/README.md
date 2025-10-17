# Frontend Documentation

## Overview

React-based frontend for the Online Quiz Application with modern UI/UX.

## Setup

```bash
npm install
npm start       # Development mode
npm run build   # Production build
```

## Project Structure

```
src/
├── components/
│   ├── Home.js          # Landing page with category selection
│   ├── Quiz.js          # Main quiz interface
│   └── Results.js       # Results and score display
├── App.js               # Main app with routing
├── index.js             # Entry point
└── *.css                # Component styles
```

## Components

### Home Component
- Category selection
- Quiz instructions
- Start quiz button

### Quiz Component
- Question display
- Answer selection
- Navigation (Previous/Next)
- Progress tracking
- Timer
- Question navigator

### Results Component
- Score summary
- Statistics display
- Detailed results review
- Retake option

## Routing

```
/           - Home page
/quiz       - Quiz interface
/results    - Results page
```

## State Management

Uses React hooks:
- `useState` for local state
- `useEffect` for side effects
- `useNavigate` for routing
- `useLocation` for route state

## API Integration

All API calls use Axios:
```javascript
axios.get('/api/questions')
axios.post('/api/questions/submit', data)
```

## Styling

- Modern gradient backgrounds
- Responsive design (mobile-first)
- CSS animations and transitions
- Color-coded feedback

## Customization

### Colors
Edit CSS variables in component `.css` files:
- Primary: `#667eea`
- Secondary: `#764ba2`
- Success: `#28a745`
- Danger: `#dc3545`

### Layout
Modify component JSX and corresponding CSS files.
