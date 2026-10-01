from flask import Flask, jsonify, request

app = Flask(__name__)

books = []
next_book_id = 1

members = []
next_member_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/api/books")
def get_books():
    return jsonify(books=books)


@app.get("/api/members")
def get_members():
    return jsonify(members=members)


@app.post("/api/members")
def create_member():
    global next_member_id

    data = request.get_json()

    member = {
        "id": next_member_id,
        "name": data["name"],
        "email": data["email"],
    }

    members.append(member)
    next_member_id += 1

    return jsonify(member), 201


@app.get("/api/members/<int:member_id>")
def get_member(member_id):
    for member in members:
        if member["id"] == member_id:
            return jsonify(member)
    return jsonify(error="Member not found"), 404


@app.put("/api/members/<int:member_id>")
def update_member(member_id):
    data = request.get_json()

    for member in members:
        if member["id"] == member_id:
            member["name"] = data["name"]
            member["email"] = data["email"]

            return jsonify(member)
    return jsonify(error="Member not found"), 404


@app.delete("/api/members/<int:member_id>")
def delete_member(member_id):
    for member in members:
        if member["id"] == member_id:
            members.remove(member)
            return jsonify(message="Member deleted")

    return jsonify(error="Member not found"), 404


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


@app.put("/api/books/<int:book_id>")
def update_book(book_id):
    data = request.get_json()

    for book in books:
        if book["id"] == book_id:
            book["title"] = data["title"]
            book["author"] = data["author"]
            book["isbn"] = data["isbn"]

            return jsonify(book)
    return jsonify(error="Book not found"), 404


@app.delete("/api/books/<int:book_id>")
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return jsonify(message="Book deleted")
    return jsonify(error="Book not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
