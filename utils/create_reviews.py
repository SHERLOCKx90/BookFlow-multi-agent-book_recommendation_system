import pandas as pd

# Sample data for reviews
reviews_data = {
    "ISBN": ["034545104X", "0385504209", "0061076031"],
    "review": [
        "An inspiring book with a positive message.",
        "Quite thrilling and suspenseful, a great read!",
        "The book was a bit slow, but had great characters."
    ]
}

# Convert to DataFrame
reviews_df = pd.DataFrame(reviews_data)

# Save to CSV
reviews_df.to_csv('data/reviews.csv', index=False, sep=';')
