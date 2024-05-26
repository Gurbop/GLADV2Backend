from flask import Blueprint, jsonify
from flask_restful import Api, Resource, request
from __init__ import app, db
from model.Books import Book

books_api = Blueprint('books', __name__, url_prefix='/api/books')
api = Api(books_api)

class BookAPI:

    class _BookList(Resource):
        def get(self):
            books = [book.all_details() for book in Book.query.all()]
            return jsonify(books)

    class _BookDetail(Resource):
        def get(self, isbn10):
            book = Book.query.filter_by(isbn10=isbn10).first()
            if book:
                return jsonify(book.all_details())
            else:
                return {'message': 'Book not found'}, 404

    class _AddBook(Resource):
        def post(self):
            data = request.get_json()
            try:
                new_book = Book(
                    isbn10=data['isbn10'],
                    title=data['title'],
                    subtitle=data.get('subtitle'),
                    authors=data.get('authors'),
                    categories=data.get('categories'),
                    thumbnail=data.get('thumbnail'),
                    description=data.get('description'),
                    published_year=data.get('published_year'),
                    average_rating=data.get('average_rating'),
                    num_pages=data.get('num_pages'),
                    ratings_count=data.get('ratings_count')
                )
                db.session.add(new_book)
                db.session.commit()
                return jsonify(new_book.all_details())
            except Exception as e:
                db.session.rollback()
                return {'message': str(e)}, 500

api.add_resource(BookAPI._BookList, '/')
api.add_resource(BookAPI._BookDetail, '/<string:isbn10>')
api.add_resource(BookAPI._AddBook, '/add')