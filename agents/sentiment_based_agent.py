from transformers import pipeline
import pandas as pd

class SentimentBasedAgent:
    def __init__(self, reviews_df):
        self.reviews_df = reviews_df
        # Specify the sentiment analysis model explicitly
        self.sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

    def recommend(self, isbn, top_n=5):
        # Filter reviews for the specific ISBN
        book_reviews = self.reviews_df[self.reviews_df['ISBN'] == isbn].copy()  # Use .copy() to avoid SettingWithCopyWarning
        if book_reviews.empty:
            print("No reviews found for the specified book.")
            return []

        # Analyze sentiment for each review
        book_reviews.loc[:, 'sentiment_score'] = book_reviews['review'].apply(
            lambda x: self.sentiment_analyzer(x)[0]['score'] if self.sentiment_analyzer(x)[0]['label'] == 'POSITIVE' else 0
        )

        # Sort reviews by sentiment score in descending order and get top N
        top_reviews = book_reviews.nlargest(top_n, 'sentiment_score')
        
        # Return the ISBNs for the books with the highest positive sentiment
        return top_reviews['ISBN'].tolist()
