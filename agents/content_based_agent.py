from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedAgent:
    def __init__(self, books_df):
        # Ensure no chained assignment warning by using fillna on a copy of DataFrame
        self.books_df = books_df.copy()
        
        # Replace NaN values with empty strings for specific columns
        self.books_df.fillna({'Book-Title': '', 'Book-Author': ''}, inplace=True)
        
        # Combine title and author as a "content" feature
        self.books_df['content'] = self.books_df['Book-Title'] + ' ' + self.books_df['Book-Author']
        
        # Initialize the TF-IDF vectorizer and compute the matrix
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.book_matrix = self.vectorizer.fit_transform(self.books_df['content'])

    def recommend(self, isbn, top_n=5):
        # Check if ISBN exists in the data
        if isbn not in self.books_df['ISBN'].values:
            print("Book not found in dataset.")
            return []

        book_idx = self.books_df.index[self.books_df['ISBN'] == isbn][0]
        cosine_similarities = cosine_similarity(self.book_matrix[book_idx], self.book_matrix).flatten()
        similar_books = cosine_similarities.argsort()[-top_n:][::-1]
        return self.books_df.iloc[similar_books]['ISBN'].tolist()
