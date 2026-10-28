from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Library Management API",
    description="Week 1 Capstone Project - CRUD, Filtering, Response Model, and Validation",
    version="1.0.0",
)

# --- 1. PYDANTIC SCHEMAS ---


class BookCreate(BaseModel):
    title: str = Field(
        min_length=1, max_length=100, description="Book title cannot be empty"
    )
    author: str = Field(min_length=2, max_length=50)
    page_count: int = Field(gt=0, description="Page count must be greater than 0")
    category: str = Field(default="General")
    cost_price: float = Field(gt=0, description="Internal cost data - Hidden")
    is_borrowed: bool = Field(default=False)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    page_count: int
    category: str
    is_borrowed: bool


# --- 2. DATA SOURCE (In-Memory Simulation) ---
BOOKS = [
    {
        "id": 1,
        "title": "Dune",
        "author": "Frank Herbert",
        "page_count": 700,
        "category": "Science Fiction",
        "cost_price": 180.0,
        "is_borrowed": False,
    },
    {
        "id": 2,
        "title": "The Dark Forest",
        "author": "Cixin Liu",
        "page_count": 510,
        "category": "Science Fiction",
        "cost_price": 140.0,
        "is_borrowed": True,
    },
    {
        "id": 3,
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "page_count": 680,
        "category": "Classic",
        "cost_price": 95.0,
        "is_borrowed": False,
    },
]


# --- 3. EXCEPTION HANDLING ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "error": exc.detail,
            "path": str(request.url.path),
        },
    )


# --- 4. ENDPOINTS ---


# 1. READ ALL: Filtering and Pagination
@app.get("/books", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def list_books(
    category: Optional[str] = Query(default=None, description="Filter by category"),
    is_borrowed: Optional[bool] = Query(
        default=None, description="Filter by borrowed status"
    ),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        default=10, ge=1, le=50, description="Maximum records to return"
    ),
):
    results = BOOKS

    if category:
        results = [b for b in results if b["category"].lower() == category.lower()]

    if is_borrowed is not None:
        results = [b for b in results if b["is_borrowed"] == is_borrowed]

    return results[skip : skip + limit]


# 2. READ ONE: Get a single book
@app.get(
    "/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK
)
def get_book(book_id: int):
    for b in BOOKS:
        if b["id"] == book_id:
            return b
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )


# 3. CREATE: Add new book
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate):
    new_id = max([b["id"] for b in BOOKS], default=0) + 1
    book_dict = book_in.model_dump()
    book_dict["id"] = new_id
    BOOKS.append(book_dict)
    return book_dict


# 4. UPDATE: Update book
@app.put(
    "/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK
)
def update_book(book_id: int, book_in: BookCreate):
    for index, b in enumerate(BOOKS):
        if b["id"] == book_id:
            updated_book = book_in.model_dump()
            updated_book["id"] = book_id
            BOOKS[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )


# 5. DELETE: Remove book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for index, b in enumerate(BOOKS):
        if b["id"] == book_id:
            BOOKS.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found",
    )
