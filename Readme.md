# Book Store FastAPI Project

## Description

This project is a simple RESTful API for managing a collection of books, built with FastAPI.  
It allows users to view all books, search for books by title, filter by category, and find books by author and category.  
The API is designed for demonstration and learning purposes, providing a foundation for building more complex book management systems.

## Setup

1. Create and activate a virtual environment:
    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the app:
    ```
    uvicorn app.books:app --reload
    ```

## API Endpoints

- `/api-endpoints` — List all books
- `/books/{book_title}` — Get book by title
- `/books/?category={category}` — Get books by category
- `/books/{book_author}/?category={category}` — Get books by