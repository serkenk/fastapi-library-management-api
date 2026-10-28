# FastAPI Library Management API

In-memory book management REST API built with FastAPI, Pydantic v2, and custom exception handling.

## Features
- Full CRUD Support: Endpoints for creating, reading, updating, and deleting books (`/books`).
- Data Validation & Sanitization: Strict schema definitions using Pydantic v2 (`BookCreate`, `BookResponse`).
- Data Isolation: Internal cost data (`cost_price`) is excluded from client responses via response models.
- Filtering & Pagination: Query parameters for category, loan status (`is_borrowed`), and offset/limit pagination.
- Custom Exception Handling: Centralized exception handler for structured JSON error responses.

## Tech Stack
- Python 3.11.9
- FastAPI
- Uvicorn
- Pydantic v2

## Getting Started

1. Clone the Repository
git clone https://github.com/serkenk/fastapi-library-management-api.git
cd fastapi-library-management-api

2. Set Up Virtual Environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
uvicorn main:app --reload

Interactive API documentation (Swagger UI):
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)