from __init__ import app, db
from flask_login import UserMixin
import os
from sqlalchemy.exc import IntegrityError
import pandas as pd

class Book(db.Model, UserMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn10 = db.Column(db.String(10), unique=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    subtitle = db.Column(db.String(256), nullable=True)
    authors = db.Column(db.String(256), nullable=True)
    categories = db.Column(db.String(256), nullable=True)
    thumbnail = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    published_year = db.Column(db.Integer, nullable=True)
    average_rating = db.Column(db.Float, nullable=True)
    num_pages = db.Column(db.Integer, nullable=True)
    ratings_count = db.Column(db.Integer, nullable=True)

    def __init__(self, isbn10, title, subtitle, authors, categories, thumbnail, description, published_year, average_rating, num_pages, ratings_count):
        self.isbn10 = isbn10
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.categories = categories
        self.thumbnail = thumbnail
        self.description = description
        self.published_year = published_year
        self.average_rating = average_rating
        self.num_pages = num_pages
        self.ratings_count = ratings_count

    def all_details(self):
        return {
            "id": self.id,
            "isbn10": self.isbn10,
            "title": self.title,
            "subtitle": self.subtitle,
            "authors": self.authors,
            "categories": self.categories,
            "thumbnail": self.thumbnail,
            "description": self.description,
            "published_year": self.published_year,
            "average_rating": self.average_rating,
            "num_pages": self.num_pages,
            "ratings_count": self.ratings_count
        }

    def few_details(self):
        return {
            "id": self.id,
            "isbn10": self.isbn10,
            "title": self.title,
            "authors": self.authors,
            "thumbnail": self.thumbnail,
            "average_rating": self.average_rating
        }

def init_books():
    with app.app_context():
        print("Initializing Books")
        """Create database and tables"""
        db.create_all()
        book_count = db.session.query(Book).count()
        if book_count > 0:
            return

        basedir = os.path.abspath(os.path.dirname(__file__))
        # Specify the file path
        file_path = os.path.join(basedir, "../static/data/books.csv")
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            try:
                book = Book(
                    isbn10=str(row['isbn10']).strip() if pd.notna(row['isbn10']) else None,
                    title=row['title'].strip() if pd.notna(row['title']) else None,
                    subtitle=row['subtitle'].strip() if pd.notna(row['subtitle']) else None,
                    authors=row['authors'].strip() if pd.notna(row['authors']) else None,
                    categories=row['categories'].strip() if pd.notna(row['categories']) else None,
                    thumbnail=row['thumbnail'].strip() if pd.notna(row['thumbnail']) else None,
                    description=row['description'].strip() if pd.notna(row['description']) else None,
                    published_year=int(row['published_year']) if pd.notna(row['published_year']) else None,
                    average_rating=float(row['average_rating']) if pd.notna(row['average_rating']) else None,
                    num_pages=int(row['num_pages']) if pd.notna(row['num_pages']) else None,
                    ratings_count=int(row['ratings_count']) if pd.notna(row['ratings_count']) else None
                )
                db.session.add(book)
                db.session.commit()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.rollback()
                print(f"Records exist, duplicate book, or error: {book.isbn10}")
            except Exception as e_inner:
                print(f"Error adding book at index {index}: {str(e_inner)}")