# adaptability_metrics.py
import torch
import random
from main import get_user_state, rl_agent, agent_selection_count, collaborative_agent, content_based_agent, sentiment_agent, ratings_df, books_df, users_df

def calculate_exploration_rate(agent_selection_count, total_iterations):
    return {agent: count / total_iterations for agent, count in agent_selection_count.items()}

def calculate_agent_success_rate(reward_per_agent):
    return {agent: sum(rewards) / len(rewards) if rewards else 0 for agent, rewards in reward_per_agent.items()}

def test_adaptability(num_iterations=100):
    reward_per_agent = {agent: [] for agent in range(3)}
    total_regret = 0

    # Filter for users and books present in both ratings and reviews
    valid_users = users_df[users_df['User-ID'].isin(ratings_df['User-ID'])]['User-ID'].tolist()
    valid_books = books_df[books_df['ISBN'].isin(ratings_df['ISBN'])]['ISBN'].tolist()

    for _ in range(num_iterations):
        user_id = random.choice(valid_users)
        example_isbn = random.choice(valid_books)
        state = get_user_state(user_id)

        action = rl_agent.select_action(state)
        agent_selection_count[action] += 1

        # Simulate the recommendation process and fallback
        fallback_used = False
        if action == 0:
            recommendations = collaborative_agent.recommend(user_id)
            if not recommendations:
                recommendations = content_based_agent.recommend(example_isbn)
                fallback_used = True
        elif action == 1:
            recommendations = content_based_agent.recommend(example_isbn)
        elif action == 2:
            recommendations = sentiment_agent.recommend(example_isbn)
            if not recommendations:
                recommendations = content_based_agent.recommend(example_isbn)
                fallback_used = True
        else:
            recommendations = []

        # Refined reward based on fallback usage and user ratings
        if recommendations:
            user_ratings = ratings_df[(ratings_df['User-ID'] == user_id) & (ratings_df['ISBN'].isin(recommendations))]
            reward = torch.tensor(user_ratings['Book-Rating'].mean() / 10 if not user_ratings.empty else 0.2)
        else:
            reward = torch.tensor(-0.1)

        if fallback_used:
            reward *= 0.8

        reward_per_agent[action].append(reward.item())
        optimal_reward = max(reward_per_agent.values(), default=[reward])[0]
        regret = optimal_reward - reward
        total_regret += regret.item()

    exploration_rate = calculate_exploration_rate(agent_selection_count, num_iterations)
    agent_success_rate = calculate_agent_success_rate(reward_per_agent)
    average_regret = total_regret / num_iterations

    return {
        "Exploration Rate": exploration_rate,
        "Agent Success Rate": agent_success_rate,
        "Average Regret": average_regret
    }
