from src.app import app

def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready():
    client = app.test_client()

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ready"}


def test_get_books():
    client = app.test_client()

    response = client.get("/api/books")

    assert response.status_code == 200
    assert response.get_json() == {"books": []}


def test_create_book():
    client = app.test_client()

    response = client.post(
        "/api/books",
        json={
            "title": "Der Hobbit",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "title": "Der Hobbit",
        "author": "J. R. R. Tolkien",
        "isbn": "9780007525515",
    }


def test_get_book():
    client = app.test_client()

    response = client.get("/api/books/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "title": "Der Hobbit",
        "author": "J. R. R. Tolkien",
        "isbn": "9780007525515",
    }


def test_get_book_not_found():
    client = app.test_client()

    response = client.get("/api/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
