from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Book, Rating, Review
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    books = Book.query.filter(Book.title.contains(query) | Book.author.contains(query)).all()
    return render_template('search.html', books=books)

@main.route('/recommendations')
@login_required
def recommendations():
    # Call recommendation system with current_user.user_id
    recommended_books = []  # Placeholder for actual recommendations
    return render_template('recommendations.html', recommended_books=recommended_books)

@main.route('/review/<int:book_id>', methods=['GET', 'POST'])
@login_required
def review(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        review_text = request.form.get('review')
        # Compute sentiment score here
        sentiment_score = 0.5  # Placeholder
        review = Review(user_id=current_user.user_id, book_id=book_id, review=review_text, sentiment_score=sentiment_score)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('main.recommendations'))
    return render_template('review.html', book=book)
