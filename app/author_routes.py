from app import db
from app.models.author import Author
from app.models.book import Book
from app.book_routes import validate_model
from flask import Blueprint, jsonify, make_response, request

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")


@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name}"
                                 "successfully created"), 201)


@authors_bp.route("", methods=["GET"])
def read_all_authors():

    authors = Author.query.all()

    authors_response = [author.to_dict() for author in authors]

    return jsonify(authors_response)


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"],
                    author=author)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by"
                                 f"{new_book.author.name}"
                                 "successfully created"), 201)


@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books_by_author(author_id):

    author = validate_model(Author, author_id)

    books_response = [book.to_dict() for book in author.books]

    return jsonify(books_response)

