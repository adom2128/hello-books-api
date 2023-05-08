from app import db
from app.book_routes import validate_model
from app.models.genre import Genre
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

genres_bp = Blueprint("genres_bp", __name__, url_prefix="/genres")


@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = request.get_json()
    new_genre = Genre.from_dict(request_body)

    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name}"
                                 " successfully created"), 201)

@genres_bp.route("", methods=["GET"])
def read_all_genres():

    genres = Genre.query.all()

    genres_response = [genre.to_dict() for genre in genres]

    return jsonify(genres_response)


@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_book_with_genre(genre_id):

    genre = validate_model(Genre, genre_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author_id=request_body["author_id"],
        genres=[genre]
    )

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by"
                                 f" {new_book.author.name} "
                                 "successfully created"), 201)


@genres_bp.route("/<genre_id>/books", methods=["GET"])
def read_books_under_genre(genre_id):

    genre = validate_model(Genre, genre_id)

    books_response = [book.to_dict() for book in genre.books]

    return jsonify(books_response)