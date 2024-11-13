
# 🔖📖 BookFlow: Multi-Agent based Book Recommendation System

A hybrid recommendation system that combines collaborative filtering, content-based filtering, and sentiment analysis with reinforcement learning to provide personalized book recommendations. This system uses real-time feedback and continuous learning to adapt to users’ preferences dynamically.

## Table of Contents
- [Project Description](#project-description)
- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Project Description
This book recommendation system is designed to offer users personalized book suggestions based on their interaction history, demographic data, and review sentiments. The system uses reinforcement learning to select the optimal recommendation method (collaborative, content-based, or sentiment-based) dynamically, improving accuracy and user satisfaction.

## Key Features
- **Hybrid Model:** Combines collaborative, content-based, and sentiment-based filtering techniques.
- **Real-Time Adaptability:** Reinforcement learning optimizes recommendations dynamically.
- **User Sentiment Analysis:** Analyzes user reviews to enhance personalization.
- **Scalable Database Integration:** MySQL database stores user, book, and interaction data.

## Architecture Overview
1. **User Interface Layer:** Manages user interactions (registration, login, book search, and reviews).
2. **Recommendation Engine Layer:** Combines the collaborative, content-based, and sentiment-based filtering agents.
3. **Data Management Layer:** Uses MySQL to store user data, ratings, reviews, and book metadata.

Refer to the `architecture_diagram.png` file for a high-level overview of data flow.

## Technologies Used
- **Python:** Core programming language
- **Flask:** Web framework for developing the application
- **SQLAlchemy:** ORM for managing database interactions
- **MySQL:** Database management system
- **PyTorch:** Used for reinforcement learning
- **Scikit-Learn:** For collaborative and content-based filtering
- **Hugging Face Transformers:** Sentiment analysis with BERT model
- **Pandas and Numpy:** Data manipulation and processing

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL server
- Git

### Setup Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/book-recommendation-system.git
   cd book-recommendation-system
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up MySQL Database:**
   - Create a MySQL database:
     ```sql
     CREATE DATABASE book_recommendation_db;
     ```
   - Update your configuration file (`config.py`) with the database credentials:
     ```python
     SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/book_recommendation_db'
     SECRET_KEY = 'your_secret_key'
     ```

5. **Initialize Database Tables:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Download and Set Up the Dataset:**
   - Download the datasets for books, users, reviews, and ratings.
   - Place them in the `data/` folder.
   - Run any necessary data preprocessing scripts if needed.

### Configuration
Create a `.env` file with your environment variables:
```bash
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=mysql+mysqlconnector://root@localhost/book_recommendation_db
SECRET_KEY=your_secret_key
```

## Usage
1. **Run the Flask Application:**
   ```bash
   flask run
   ```
2. **Access the Application:**
   Open a web browser and go to `http://127.0.0.1:5000`.

3. **User Actions:**
   - **Register and Log In:** Users can register and log in to the application.
   - **Search and Review Books:** Search for books by title, author, or ISBN, and submit reviews.
   - **View Recommendations:** See personalized book recommendations based on user preferences and feedback.

## Project Structure
```
book-recommendation-system/
│
├── app/                       # Flask application files
│   ├── __init__.py            # App initialization
│   ├── models.py              # Database models for Users, Books, Ratings, Reviews
│   ├── routes.py              # Application routes
│   └── templates/             # HTML templates for UI
│
├── data/                      # Dataset files
│
├── agents/                    # Recommendation agents
│   ├── collaborative_agent.py # Collaborative filtering logic
│   ├── content_based_agent.py # Content-based filtering logic
│   └── sentiment_based_agent.py # Sentiment analysis logic
│
├── rl_model/                  # Reinforcement learning components
│   ├── actor_critic.py        # Actor-Critic model for agent selection
│
├── config.py                  # Configuration settings
├── requirements.txt           # Required packages
└── README.md                  # Project documentation
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

⚠️ Note: Make sure to replace placeholder text, such as `your-username` and `your_secret_key`, with your actual information.
