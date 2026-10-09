import pytest

from src import app as app_module

app = app_module.app


@pytest.fixture(autouse=True)
def reset_state():
    app_module.books.clear()
    app_module.members.clear()
    app_module.next_book_id = 1
    app_module.next_member_id = 1
    yield


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
        "status": "available",
        "borrowed_to": None,
    }


def test_get_book():
    client = app.test_client()

    created = client.post(
        "/api/books",
        json={
            "title": "Der Hobbit",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )
    book_id = created.get_json()["id"]

    response = client.get(f"/api/books/{book_id}")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": book_id,
        "title": "Der Hobbit",
        "author": "J. R. R. Tolkien",
        "isbn": "9780007525515",
        "status": "available",
        "borrowed_to": None,
    }


def test_get_book_not_found():
    client = app.test_client()

    response = client.get("/api/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}


def test_update_book():
    client = app.test_client()

    created = client.post(
        "/api/books",
        json={
            "title": "Der Hobbit",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )
    book_id = created.get_json()["id"]

    response = client.put(
        f"/api/books/{book_id}",
        json={
            "title": "Der Hobbit - Neue Ausgabe",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": book_id,
        "title": "Der Hobbit - Neue Ausgabe",
        "author": "J. R. R. Tolkien",
        "isbn": "9780007525515",
        "status": "available",
        "borrowed_to": None,
    }


def test_delete_book():
    client = app.test_client()

    created = client.post(
        "/api/books",
        json={
            "title": "Der Hobbit",
            "author": "J. R. R. Tolkien",
            "isbn": "9780007525515",
        },
    )
    book_id = created.get_json()["id"]

    response = client.delete(f"/api/books/{book_id}")

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
        "borrowed_books": [],
        "borrowed_count": 0,
    }


def test_index_page_renders():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Library" in response.data


def test_books_page_renders():
    client = app.test_client()

    response = client.get("/books")

    assert response.status_code == 200
    assert b"Books" in response.data


def test_members_page_renders():
    client = app.test_client()

    response = client.get("/members")

    assert response.status_code == 200
    assert b"Members" in response.data


def test_get_member():
    client = app.test_client()

    created = client.post(
        "/api/members",
        json={
            "name": "Max Bücherwurm",
            "email": "max@wurm.ch",
        },
    )
    member_id = created.get_json()["id"]

    response = client.get(f"/api/members/{member_id}")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": member_id,
        "name": "Max Bücherwurm",
        "email": "max@wurm.ch",
        "borrowed_books": [],
        "borrowed_count": 0,
    }


def test_get_member_not_found():
    client = app.test_client()

    response = client.get("/api/members/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Member not found"}


def test_update_member():
    client = app.test_client()

    created = client.post(
        "/api/members",
        json={
            "name": "Max Bücherwurm",
            "email": "max@wurm.ch",
        },
    )
    member_id = created.get_json()["id"]

    response = client.put(
        f"/api/members/{member_id}",
        json={
            "name": "Max Lesemaus",
            "email": "max@maus.ch",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": member_id,
        "name": "Max Lesemaus",
        "email": "max@maus.ch",
        "borrowed_books": [],
        "borrowed_count": 0,
    }


def test_delete_member():
    client = app.test_client()

    created = client.post(
        "/api/members",
        json={
            "name": "Max Bücherwurm",
            "email": "max@wurm.ch",
        },
    )
    member_id = created.get_json()["id"]

    response = client.delete(f"/api/members/{member_id}")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Member deleted"}


def test_delete_member_not_found():
    client = app.test_client()

    response = client.delete("/api/members/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Member not found"}


def test_borrow_book_and_show_member_loans():
    client = app_module.app.test_client()

    book_response = client.post(
        "/api/books",
        json={
            "title": "Pippi Langstrumpf",
            "author": "Astrid Lindgren",
            "isbn": "9783499227277",
        },
    )
    member_response = client.post(
        "/api/members",
        json={
            "name": "Anna Leseratte",
            "email": "anna@lese.ch",
        },
    )

    book_id = book_response.get_json()["id"]
    member_id = member_response.get_json()["id"]

    response = client.post(
        f"/api/books/{book_id}/borrow",
        json={"member_id": member_id},
    )

    assert response.status_code == 200
    assert response.get_json()["message"] == "Book borrowed successfully"
    assert response.get_json()["book"]["status"] == "borrowed"
    assert response.get_json()["book"]["borrowed_to"] == member_id

    member_response = client.get(f"/api/members/{member_id}")
    assert member_response.status_code == 200
    assert member_response.get_json()["borrowed_count"] == 1
    assert len(member_response.get_json()["borrowed_books"]) == 1
    assert member_response.get_json()["borrowed_books"][0]["title"] == "Pippi Langstrumpf"

    book_response = client.get(f"/api/books/{book_id}")
    assert book_response.status_code == 200
    assert book_response.get_json()["status"] == "borrowed"
    assert book_response.get_json()["borrowed_to"] == member_id
