### Flask REST API with User Authentication

This is a REST API in python using Flask for a library of books. Users can sign up and add, view, update and delete books.

#### Prequisites

- SQLite
- Postman

#### Instructions

1. Download and install SQLite
2. In project folder, create a python virtual environment `python -m venv env` and activate it `env\Scripts\activate`
4. Install required libraries `pip install -r requirements.txt`
5. Run `python app.py`
6. Use Postman to access the end-points and examples below with url prefix `http://localhost:8000/api/v1`

#### End-points

- GET /books (View all books)
- GET /books/:id (Get book by ID)
- POST /users (Add a user)
`
{
	"username": "admin",
	"password": "password1"
}
`
- \*POST /books (Add a book)
`
{
	"title": "Grokking Algorithms",
	"author": "Aditya Bhargava"
}
`
- \*PUT /books/:id (Update a book by ID)
- \*DELETE /books/:id (Delete a book by ID)

\*User authentication required