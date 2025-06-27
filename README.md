Book Review API (FastAPI + Redis Cache)

This project is a simple RESTful API for managing books and their reviews. It is built using FastAPI, SQLAlchemy, SQLite, and Redis, with unit/integration testing using pytest.

## Goal of the Project

- Add and view books
- Add and view reviews for each book
- Redis caching for book list (GET /books)
- Automatic cache population on cache-miss
- Unit and integration tests with pytest

## Tech Stack

- Backend : FastAPI
- Database : SQLite + SQLAlchemy
- Cache : Redis
- Testing : Pytest, TestClient

## Folder Structure Overview

book_review_api/
├── main.py # Entry point for FastAPI app and all routes
├── models.py # write all database tables
├── schemas.py # Request/Response data models using Pydantic
├── venv # virtualenvironment
├── crud.py # Functions to interact with the database (Create, Read)
├── database.py # SQLite database engine and session setup
├── cache.py # Redis setup and cache management
├── test_main.py # Unit and integration tests using pytest
├── alembic/ # Auto-generated DB migration files
├── alembic.ini # Alembic settings (DB URL, etc.)
├── requirements.txt # Python dependencies
└── README.md # This file

## Installation

- open git bash or terminal
- git clone https://github.com/your-username/book-review-api.git
<!-- - cd book-review-api -->
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt

## Run the API Server

- uvicorn main:app --reload
- Now open: http://localhost:8000/docs
- Here i tested all endpoints via Swagger UI.

## Database Migrations with Alembic

- Alembic tracks the developer made changes and apply them to the database.
- alembic init alembic (Initialize Alembic)
- alembic revision --autogenerate -m "create books and reviews tables" (generate migration files)
- alembic upgrade head (apply migration)

## Testing the API

- pytest test_main.py
- it includes
- Creating a new book
- Fetching all books
- Verifying data structure and behavior
- pytest test_main.py (run tests)
