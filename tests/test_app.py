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