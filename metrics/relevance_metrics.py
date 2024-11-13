# relevance_metrics.py
import random
import numpy as np
from main import get_user_state, collaborative_agent, content_based_agent, sentiment_agent, ratings_df, books_df, users_df

def calculate_precision(true_positive, false_positive):
    return true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0

def calculate_recall(true_positive, false_negative):
    return true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0

def mean_reciprocal_rank(ranked_list):
    for i, item in enumerate(ranked_list, start=1):
        if item:
            return 1 / i
    return 0

def test_relevance(num_iterations=100):
    precision_scores = []
    recall_scores = []
    mrr_scores = []

    # Filter for users and books present in ratings and reviews
    valid_users = users_df[users_df['User-ID'].isin(ratings_df['User-ID'])]['User-ID'].tolist()
    valid_books = books_df[books_df['ISBN'].isin(ratings_df['ISBN'])]['ISBN'].tolist()

    for _ in range(num_iterations):
        user_id = random.choice(valid_users)
        example_isbn = random.choice(valid_books)
        state = get_user_state(user_id)

        action = random.choice([0, 1, 2])
        if action == 0:
            recommendations = collaborative_agent.recommend(user_id)
            if not recommendations:
                recommendations = content_based_agent.recommend(example_isbn)
        elif action == 1:
            recommendations = content_based_agent.recommend(example_isbn)
        elif action == 2:
            recommendations = sentiment_agent.recommend(example_isbn)
            if not recommendations:
                recommendations = content_based_agent.recommend(example_isbn)
        else:
            recommendations = []

        relevant_set = set(ratings_df[ratings_df['User-ID'] == user_id]['ISBN'].tolist())
        if not relevant_set:
            continue

        true_positive = len([rec for rec in recommendations if rec in relevant_set])
        false_positive = len(recommendations) - true_positive
        false_negative = len(relevant_set) - true_positive

        precision_scores.append(calculate_precision(true_positive, false_positive))
        recall_scores.append(calculate_recall(true_positive, false_negative))
        mrr_scores.append(mean_reciprocal_rank([rec in relevant_set for rec in recommendations]))

    return {
        "Average Precision": np.mean(precision_scores),
        "Average Recall": np.mean(recall_scores),
        "Average MRR": np.mean(mrr_scores)
    }
