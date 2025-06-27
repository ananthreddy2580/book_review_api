import redis
import json

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    redis_available = True
except redis.ConnectionError:
    redis_available = False

def cache_available():
    return redis_available

def get_cached_books():
    books = r.get("books")
    if books:
        return json.loads(books)
    return None

def set_cached_books(data):
    r.set("books", json.dumps(data), ex=60)