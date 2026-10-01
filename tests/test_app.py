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


def test_update_book():
    client = app.test_client()

    response = client.put(
        "/api/books/1",
        json={
            "title": "Der Hobbit - Neue Ausgabe",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "title": "Der Hobbit - Neue Ausgabe",
        "author": "J. R. R. Tolkien",
        "isbn": "9780007525515",
    }


def test_delete_book():
    client = app.test_client()

    response = client.delete("/api/books/1")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Book deleted"}


def test_delete_book_not_found():
    client = app.test_client()

    response = client.delete("/api/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}


def test_get_members():
    client = app.test_client()

    response = client.get("/api/members")

    assert response.status_code == 200
    assert response.get_json() == {"members": []}


def test_create_member():
    client = app.test_client()

    response = client.post(
        "/api/members",
        json={
            "name": "Max Bücherwurm",
            "email": "max@wurm.ch",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Max Bücherwurm",
        "email": "max@wurm.ch",
    }


def test_get_member():
    client = app.test_client()

    response = client.get("/api/members/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Max Bücherwurm",
        "email": "max@wurm.ch",
    }


def test_get_member_not_found():
    client = app.test_client()

    response = client.get("/api/members/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Member not found"}


def test_update_member():
    client = app.test_client()

    response = client.put(
        "/api/members/1",
        json={
            "name": "Max Lesemaus",
            "email": "max@maus.ch",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "name": "Max Lesemaus",
        "email": "max@maus.ch",
    }


def test_delete_member():
    client = app.test_client()

    response = client.delete("/api/members/1")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Member deleted"}


def test_delete_member_not_found():
    client = app.test_client()

    response = client.delete("/api/members/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Member not found"}
