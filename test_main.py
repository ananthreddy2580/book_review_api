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
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.delete("books")
    
    book_payload = {
        "title": "Cache Miss Book",
        "author": "Tester"
    }
    post_response = client.post("/books", json=book_payload)
    assert post_response.status_code == 200
    new_book = post_response.json()

    assert r.get("books") is None

    get_response = client.get("/books")
    assert get_response.status_code == 200
    books = get_response.json()

    assert any(book["title"] == "Cache Miss Book" for book in books)

    cached = r.get("books")
    assert cached is not None
    cached_books = json.loads(cached)
    assert any(book["title"] == "Cache Miss Book" for book in cached_books)
