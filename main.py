import torch
import pandas as pd
import random
from agents.collaborative_agent import CollaborativeFilteringAgent
from agents.content_based_agent import ContentBasedAgent
from agents.sentiment_based_agent import SentimentBasedAgent
from rl_model.actor_critic import ActorCriticAgent

# Load data
books_df = pd.read_csv(
    'data/books_final_cleaned.csv',
    delimiter=';',
    encoding='ISO-8859-1',
    dtype={
        'ISBN': str,
        'Book-Title': str,
        'Book-Author': str,
        'Year-Of-Publication': str,
        'Publisher': str,
        'Image-URL-S': str,
        'Image-URL-M': str,
        'Image-URL-L': str
    },
    low_memory=False
)
ratings_df = pd.read_csv('data/ratings_corrected.csv', delimiter=';', encoding='ISO-8859-1')
reviews_df = pd.read_csv('data/reviews.csv', delimiter=';', encoding='ISO-8859-1')
users_df = pd.read_csv('data/users.csv', delimiter=';', encoding='ISO-8859-1')

# Initialize agents
collaborative_agent = CollaborativeFilteringAgent(ratings_df)
content_based_agent = ContentBasedAgent(books_df)
sentiment_agent = SentimentBasedAgent(reviews_df)

# Initialize reinforcement learning agent (Actor-Critic model)
num_agents = 3  # Three agents: collaborative, content-based, and sentiment-based
rl_agent = ActorCriticAgent(num_agents)

# Track agent selection count and performance
agent_selection_count = {0: 0, 1: 0, 2: 0}

# Helper function to get demographic-based state
def get_user_state(user_id):
    user_data = users_df[users_df['User-ID'] == user_id]
    if not user_data.empty:
        age = user_data['Age'].values[0] if pd.notnull(user_data['Age'].values[0]) else 35  # Default age
        location_score = len(user_data['Location'].values[0]) % 10 / 10  # Example location-based score
        return torch.tensor([[age / 100, location_score, 0.5]], dtype=torch.float32)
    else:
        return torch.tensor([[0.5, 0.5, 0.5]], dtype=torch.float32)  # Default state if user not found

# Recommendation Process with refined reward structure
for i in range(5):
    user_id = random.choice(users_df['User-ID'].tolist())
    example_isbn = random.choice(books_df['ISBN'].tolist())
    state = get_user_state(user_id)

    action = rl_agent.select_action(state)
    agent_selection_count[action] += 1

    fallback_used = False  # Track if fallback is needed
    if action == 0:
        recommendations = collaborative_agent.recommend(user_id)
        if not recommendations:
            print("User not found or no recommendations; falling back to Content-Based Agent.")
            recommendations = content_based_agent.recommend(example_isbn)
            fallback_used = True
    elif action == 1:
        recommendations = content_based_agent.recommend(example_isbn)
    elif action == 2:
        recommendations = sentiment_agent.recommend(example_isbn)
        if not recommendations:
            print("No reviews found; falling back to Content-Based Agent.")
            recommendations = content_based_agent.recommend(example_isbn)
            fallback_used = True
    else:
        recommendations = []

    print(f"User ID: {user_id}, ISBN: {example_isbn}, Recommended Books by Agent {action}: {recommendations}")

    # Refined reward based on fallback and user ratings
    if recommendations:
        user_ratings = ratings_df[(ratings_df['User-ID'] == user_id) & (ratings_df['ISBN'].isin(recommendations))]
        if not user_ratings.empty:
            reward = torch.tensor(user_ratings['Book-Rating'].mean() / 10)
        else:
            reward = torch.tensor(0.2)  # Minimal reward if no user feedback on recommendations
    else:
        reward = torch.tensor(-0.1)  # Small penalty if no recommendations generated initially

    # Apply a penalty if fallback was required to provide recommendations
    if fallback_used:
        reward *= 0.8  # Reduce reward slightly to encourage agents with direct recommendations

    # Update Actor-Critic model
    next_state = get_user_state(user_id)
    rl_agent.update(state, action, reward, next_state)
    state = next_state

# Print agent selection counts
print("\nAgent Selection Counts:")
for agent, count in agent_selection_count.items():
    print(f"Agent {agent}: Selected {count} times")


# import torch
# import random
# from app import db  # Assuming SQLAlchemy db object is initialized in app/__init__.py
# from app.models import User, Book, Rating, Review  # Import SQLAlchemy models
# from agents.collaborative_agent import CollaborativeFilteringAgent
# from agents.content_based_agent import ContentBasedAgent
# from agents.sentiment_based_agent import SentimentBasedAgent
# from rl_model.actor_critic import ActorCriticAgent

# # Initialize agents dynamically from the database
# def load_data():
#     books_df = pd.read_sql(Book.query.statement, db.engine)
#     ratings_df = pd.read_sql(Rating.query.statement, db.engine)
#     reviews_df = pd.read_sql(Review.query.statement, db.engine)
#     users_df = pd.read_sql(User.query.statement, db.engine)
#     return books_df, ratings_df, reviews_df, users_df

# books_df, ratings_df, reviews_df, users_df = load_data()

# # Initialize recommendation agents
# collaborative_agent = CollaborativeFilteringAgent(ratings_df)
# content_based_agent = ContentBasedAgent(books_df)
# sentiment_agent = SentimentBasedAgent(reviews_df)

# # Initialize Actor-Critic model (RL Agent)
# num_agents = 3
# rl_agent = ActorCriticAgent(num_agents)

# # Track agent selection count and performance for logging
# agent_selection_count = {0: 0, 1: 0, 2: 0}

# # Helper function to get demographic-based state for RL model
# def get_user_state(user_id):
#     user = User.query.get(user_id)
#     if user:
#         age = user.age if user.age else 35
#         location_score = len(user.country) % 10 / 10
#         return torch.tensor([[age / 100, location_score, 0.5]], dtype=torch.float32)
#     else:
#         return torch.tensor([[0.5, 0.5, 0.5]], dtype=torch.float32)  # Default state

# # Function to handle recommendation process
# def recommend_books(user_id, example_isbn):
#     state = get_user_state(user_id)
#     action = rl_agent.select_action(state)
#     agent_selection_count[action] += 1
#     fallback_used = False

#     if action == 0:
#         recommendations = collaborative_agent.recommend(user_id)
#         if not recommendations:
#             print("User not found or no recommendations; falling back to Content-Based Agent.")
#             recommendations = content_based_agent.recommend(example_isbn)
#             fallback_used = True
#     elif action == 1:
#         recommendations = content_based_agent.recommend(example_isbn)
#     elif action == 2:
#         recommendations = sentiment_agent.recommend(example_isbn)
#         if not recommendations:
#             print("No reviews found; falling back to Content-Based Agent.")
#             recommendations = content_based_agent.recommend(example_isbn)
#             fallback_used = True
#     else:
#         recommendations = []

#     print(f"User ID: {user_id}, ISBN: {example_isbn}, Recommended Books by Agent {action}: {recommendations}")
    
#     reward = calculate_reward(user_id, recommendations, fallback_used)
#     update_rl_agent(state, action, reward, user_id)
#     return recommendations

# # Reward calculation based on recommendations and user feedback
# def calculate_reward(user_id, recommendations, fallback_used):
#     if recommendations:
#         user_ratings = Rating.query.filter_by(user_id=user_id).filter(Rating.book_id.in_(recommendations)).all()
#         if user_ratings:
#             reward = torch.tensor(sum([r.rating for r in user_ratings]) / len(user_ratings) / 10)
#         else:
#             reward = torch.tensor(0.2)  # Minimal reward if no feedback
#     else:
#         reward = torch.tensor(-0.1)  # Penalty if no recommendations

#     if fallback_used:
#         reward *= 0.8  # Penalty for fallback
#     return reward

# # Update RL agent with new reward and state
# def update_rl_agent(state, action, reward, user_id):
#     next_state = get_user_state(user_id)
#     rl_agent.update(state, action, reward, next_state)

# # Simulate recommendation requests for testing
# def test_recommendation_process(num_tests=5):
#     for _ in range(num_tests):
#         user_id = random.choice(users_df['user_id'].tolist())
#         example_isbn = random.choice(books_df['isbn'].tolist())
#         recommend_books(user_id, example_isbn)

#     print("\nAgent Selection Counts:")
#     for agent, count in agent_selection_count.items():
#         print(f"Agent {agent}: Selected {count} times")

# if __name__ == "__main__":
#     test_recommendation_process()
