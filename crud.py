from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException

def create_book(db, book):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db):
    return db.query(models.Book).all()

def get_book(db, book_id):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_review(db, review, book_id):
    db_review = models.Review(content=review.content, book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_for_book(db, book_id):
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

