from flask import Flask, jsonify, request

app = Flask(__name__)

books = []
next_book_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/api/books")
def get_books():
    return jsonify(books=books)


@app.get("/api/books/<int:book_id>")
def get_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return jsonify(book)
    return jsonify(error="Book not found"), 404


@app.post("/api/books")
def create_book():
    data = request.get_json()

    global next_book_id

    book = {
        "id": next_book_id,
        "title": data['title'],
        "author": data['author'],
        "isbn": data['isbn'],
    }
    
    books.append(book)
    next_book_id += 1

    return jsonify(book), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    