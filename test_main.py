from fastapi.testclient import TestClient
from main import app
import redis
import json

client = TestClient(app)

def test_create_book():
    response = client.post("/books", json={
        "title": "Test Driven Book",
        "author": "Test Author"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Driven Book"
    assert data["author"] == "Test Author"
    assert "id" in data

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cache_miss_behavior():
    # Clear Redis cache manually
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.delete("books")  # simulate cache miss

    # Add a new book (goes into DB)
    book_payload = {
        "title": "Cache Miss Book",
        "author": "Tester"
    }
    post_response = client.post("/books", json=book_payload)
    assert post_response.status_code == 200
    new_book = post_response.json()

    # Ensure cache is empty before GET
    assert r.get("books") is None

    # GET /books to simulate cache miss
    get_response = client.get("/books")
    assert get_response.status_code == 200
    books = get_response.json()

    # The new book should be in the response
    assert any(book["title"] == "Cache Miss Book" for book in books)

    # Cache should now be populated
    cached = r.get("books")
    assert cached is not None
    cached_books = json.loads(cached)
    assert any(book["title"] == "Cache Miss Book" for book in cached_books)
