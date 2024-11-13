from . import db
from flask_login import UserMixin
from . import bcrypt

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    country = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    ratings = db.relationship('Rating', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Book(db.Model):
    __tablename__ = 'Books'
    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    year_of_publication = db.Column(db.Integer)
    publisher = db.Column(db.String(255))

    ratings = db.relationship('Rating', backref='book', lazy=True)
    reviews = db.relationship('Review', backref='book', lazy=True)


class Rating(db.Model):
    __tablename__ = 'Ratings'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.book_id'), nullable=False)
    rating = db.Column(db.Integer)


class Review(db.Model):
    __tablename__ = 'Reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Books.book_id'), nullable=False)
    review = db.Column(db.Text)
    sentiment_score = db.Column(db.Float)
