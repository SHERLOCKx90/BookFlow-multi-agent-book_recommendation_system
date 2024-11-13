import os

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@localhost/book_recommendation_db'
SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')  # Replace with fallback for testing
