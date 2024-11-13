import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class CollaborativeFilteringAgent:
    def __init__(self, ratings_df):
        # Filter ratings data to avoid excessive memory use
        ratings_df = ratings_df.groupby('ISBN').filter(lambda x: len(x) > 10)  # Keep books with >10 ratings
        ratings_df = ratings_df.groupby('User-ID').filter(lambda x: len(x) > 10)  # Keep users with >10 ratings

        self.ratings_df = ratings_df
        # Create user-item matrix as a sparse matrix
        self.user_item_matrix = self.ratings_df.pivot(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
        self.user_item_sparse = csr_matrix(self.user_item_matrix.values)  # Convert to sparse format
        self.similarity_matrix = cosine_similarity(self.user_item_sparse)

    def recommend(self, user_id, top_n=5):
        # Check if user_id exists in the data
        if user_id not in self.user_item_matrix.index:
            print("User not found in dataset.")
            return []

        user_index = self.user_item_matrix.index.get_loc(user_id)
        user_similarity = self.similarity_matrix[user_index]
        
        # Compute book ratings using similarity
        book_ratings = self.user_item_sparse.T.dot(user_similarity)
        
        # Convert book ratings to Series for easy sorting and selection
        recommended_books = pd.Series(book_ratings.flatten(), index=self.user_item_matrix.columns).nlargest(top_n).index.tolist()
        
        return recommended_books
