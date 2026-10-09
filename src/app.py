from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

books = []
next_book_id = 1

members = []
next_member_id = 1


def get_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def get_member_by_id(member_id):
    for member in members:
        if member["id"] == member_id:
            return member
    return None


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/")
def index():
    return render_template("index.html", books=books, members=members)


@app.route("/books", methods=["GET", "POST"])
def books_page():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()

        if not title or not author or not isbn:
            return "Missing book data", 400

        global next_book_id
        book = {
            "id": next_book_id,
            "title": title,
            "author": author,
            "isbn": isbn,
            "status": "available",
            "borrowed_to": None,
        }
        books.append(book)
        next_book_id += 1
        return redirect(url_for("books_page"))

    return render_template("books.html", books=books, members=members)


@app.route("/members", methods=["GET", "POST"])
def members_page():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            return "Missing member data", 400

        global next_member_id
        member = {
            "id": next_member_id,
            "name": name,
            "email": email,
            "borrowed_books": [],
            "borrowed_count": 0,
        }
        members.append(member)
        next_member_id += 1
        return redirect(url_for("members_page"))

    return render_template("members.html", members=members)


@app.post("/books/<int:book_id>/borrow")
def borrow_book_ui(book_id):
    member_id = request.form.get("member_id")
    if member_id is None:
        return "Member is required", 400

    member_id = int(member_id)
    book = get_book_by_id(book_id)
    if book is None:
        return "Book not found", 404

    member = get_member_by_id(member_id)
    if member is None:
        return "Member not found", 404

    if book["status"] == "borrowed":
        return "Book already borrowed", 409

    book["status"] = "borrowed"
    book["borrowed_to"] = member_id

    if not any(loan["id"] == book_id for loan in member["borrowed_books"]):
        member["borrowed_books"].append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "isbn": book["isbn"],
        })

    member["borrowed_count"] = len(member["borrowed_books"])
    return redirect(url_for("books_page"))


@app.post("/books/<int:book_id>/return")
def return_book_ui(book_id):
    member_id = request.form.get("member_id")
    if member_id is None:
        return "Member is required", 400

    member_id = int(member_id)
    book = get_book_by_id(book_id)
    if book is None:
        return "Book not found", 404

    member = get_member_by_id(member_id)
    if member is None:
        return "Member not found", 404

    if book["status"] != "borrowed" or book["borrowed_to"] != member_id:
        return "This book is not borrowed by this member", 400

    book["status"] = "available"
    book["borrowed_to"] = None
    member["borrowed_books"] = [
        loan for loan in member["borrowed_books"] if loan["id"] != book_id
    ]
    member["borrowed_count"] = len(member["borrowed_books"])
    return redirect(url_for("books_page"))


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
        "borrowed_books": [],
        "borrowed_count": 0,
    }

    members.append(member)
    next_member_id += 1

    return jsonify(member), 201


@app.get("/api/members/<int:member_id>")
def get_member(member_id):
    member = get_member_by_id(member_id)
    if member is None:
        return jsonify(error="Member not found"), 404
    return jsonify(member)


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
    book = get_book_by_id(book_id)
    if book is not None:
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
        "status": "available",
        "borrowed_to": None,
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


@app.post("/api/books/<int:book_id>/borrow")
def borrow_book(book_id):
    data = request.get_json() or {}
    member_id = data.get("member_id")

    book = get_book_by_id(book_id)
    if book is None:
        return jsonify(error="Book not found"), 404

    member = get_member_by_id(member_id)
    if member is None:
        return jsonify(error="Member not found"), 404

    if book["status"] == "borrowed":
        return jsonify(error="Book already borrowed"), 409

    book["status"] = "borrowed"
    book["borrowed_to"] = member_id

    if not any(loan["id"] == book_id for loan in member["borrowed_books"]):
        member["borrowed_books"].append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "isbn": book["isbn"],
        })

    member["borrowed_count"] = len(member["borrowed_books"])

    return jsonify(message="Book borrowed successfully", book=book, member=member), 200


@app.post("/api/books/<int:book_id>/return")
def return_book(book_id):
    data = request.get_json() or {}
    member_id = data.get("member_id")

    book = get_book_by_id(book_id)
    if book is None:
        return jsonify(error="Book not found"), 404

    if book["status"] != "borrowed":
        return jsonify(error="Book is not currently borrowed"), 400

    member = get_member_by_id(member_id)
    if member is None:
        return jsonify(error="Member not found"), 404

    if book["borrowed_to"] != member_id:
        return jsonify(error="This book is not borrowed by this member"), 400

    book["status"] = "available"
    book["borrowed_to"] = None
    member["borrowed_books"] = [
        loan for loan in member["borrowed_books"] if loan["id"] != book_id
    ]
    member["borrowed_count"] = len(member["borrowed_books"])

    return jsonify(message="Book returned successfully", book=book, member=member), 200


@app.delete("/api/books/<int:book_id>")
def delete_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return jsonify(message="Book deleted")
    return jsonify(error="Book not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
