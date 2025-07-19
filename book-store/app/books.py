from fastapi import FastAPI , Path , Query , HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel): 
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt= -1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5 , 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5 , 2027 ),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5 , 2030),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2 , 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3 , 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1 , 2025)
]

@app.get("/books" , status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS 


@app.get("/books/{book_id}" , status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/" , status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: str = Query(gt = 0 , lt=6) ):
    filtered_books = []
    for book in BOOKS:
        if book.rating == int(rating):
            filtered_books.append(book)
    if not filtered_books:
        return {"error": "No books found with the specified rating"}
    return filtered_books

def find_book_id():
    if len(BOOKS) == 0:
        return 1
    return BOOKS[-1].id + 1

@app.get("/books/publish" , status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    filtered_books = [book for book in BOOKS if book.published_date == published_date]
    if not filtered_books:
        return {"error": "No books found for the specified published date"}
    return filtered_books

@app.post("/create_book" , status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_id = find_book_id()
    new_book = Book(**book_request.model_dump())
    new_book.id = new_id
    BOOKS.append(new_book)
    return new_book

@app.put("/books/update_book" , status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    Book_Changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            Book_Changed = True
            return BOOKS[i]
    if not Book_Changed:
        raise HTTPException(status_code=404, detail="item not found")

@app.delete("/books/{book_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    Book_Changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            Book_Changed = True
            break
    if not Book_Changed:
        raise HTTPException(status_code=404, detail="item not found")

