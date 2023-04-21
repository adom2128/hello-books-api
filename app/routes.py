from flask import Blueprint, jsonify, abort, make_response

books_bp = Blueprint("books", __name__, url_prefix="/books")


class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.description = description
        self.title = title


books = [Book(1, "Carrie Soto is Back", "tennis comeback story"), 
         Book(2, "Legends and Lattes", "low stakes fantasy in a coffee shop"), 
         Book(3, "Our Missing Hearts", "Our future after COVID, maybe")]


@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))

    for book in books:
        if book.id == book_id:
            return book

    abort(make_response({"message": f"book {book_id} not found"}, 404))


@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }
