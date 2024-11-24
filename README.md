# RevAIwer

RevAIwer is an innovative application designed to assist users in comparing movies based on ratings, prices, and other metrics. By leveraging state-of-the-art AI techniques such as Retrieval-Augmented Generation (RAG), prompt engineering, and large language models (LLMs), RevAIwer provides insightful summaries and scores for movies based on both critic and audience reviews.

---

## Features

### 🎥 Movie Review Analysis
- Summarizes critic and audience reviews to provide clear, actionable insights.
- Highlights pros, cons, and overall sentiment for each movie.

### 📊 Advanced Scoring System
- **Quality Score:** Analyzes review content and summaries for relevance.
- **Price Score:** Balances ratings and hypothetical price ranges.
- **Sentiment Score:** Evaluates sentiment expressed in reviews using keyword analysis.

### 🏆 Best Movie Selector
- Automatically compares movies and identifies the one with the best overall score.

### 🔎 Web Scraping
- Extracts reviews directly from Rotten Tomatoes using BeautifulSoup.

### 💡 AI-Powered Summaries
- Leverages AWS Bedrock Runtime with Meta Llama 3 to generate professional-quality summaries and ratings.

---

## How It Works

1. **Review Collection:**
   - Scrapes reviews for selected movies from Rotten Tomatoes (critic and audience).

2. **Summary Generation:**
   - Uses AI to craft detailed summaries and provide ratings based on storytelling, acting, visuals, and direction.

3. **Scoring System:**
   - Combines Quality, Price, and Sentiment Scores to evaluate each movie.

4. **Comparison & Selection:**
   - Determines the best movie based on scores and provides detailed feedback.

---

## Tech Stack

### Backend
- Python
- AWS Lambda for API handling
- BeautifulSoup for web scraping
- AWS Bedrock Runtime for AI integration

### Frontend
- React (with App.tsx as a core file)
- Responsive UI for user-friendly experience

### AI Models
- Meta Llama 3 for summarization
- Custom algorithms for scoring and analysis

---

## Installation

### Prerequisites
- Python 3.8+
- Node.js and npm
- AWS account with Bedrock Runtime access

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/revaiwer.git
   cd revaiwer/backend
