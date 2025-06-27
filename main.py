from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import models, schemas, crud
from database import SessionLocal, engine
from cache import get_cached_books, set_cached_books, cache_available

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@app.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    if cache_available():
        cached_data = get_cached_books()
        if cached_data:
            print("✅ Data returned from CACHE")
            return cached_data
    print("📦 Data returned from DATABASE")
    books = crud.get_books(db)
    result = [schemas.Book.model_validate(book) for book in books]


    if cache_available():
        set_cached_books([book.model_dump() for book in result])


    return result

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
def create_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_review(db, review, book_id)

@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.get_reviews_for_book(db, book_id)