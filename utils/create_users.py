import pandas as pd
import random

# Configuration for synthetic data
num_users = 1000  # Adjust the number of users as needed
locations = ["New York, USA", "London, UK", "Paris, France", "Berlin, Germany", "Tokyo, Japan", "Sydney, Australia"]
min_age, max_age = 18, 80  # Age range

# Generate user data
data = {
    "User-ID": [i for i in range(1, num_users + 1)],
    "Location": [random.choice(locations) for _ in range(num_users)],
    "Age": [random.randint(min_age, max_age) if random.random() > 0.1 else None for _ in range(num_users)]  # 10% missing ages
}

# Convert to DataFrame and save as users.csv
users_df = pd.DataFrame(data)
users_df.to_csv('data/users.csv', index=False, sep=';')

print("Generated users.csv with synthetic user data.")
