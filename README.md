# FastAPI Expense Tracker

A RESTful API built with FastAPI, SQLAlchemy, and SQLite to track personal expenses with JWT-based authentication.

## Features

- **Authentication**: User registration and JWT-based authentication (OAuth2 Password Bearer).
- **Expense Management**: Full CRUD operations for expenses (create, list, search by title, view details, update, and delete).
- **User Management**: Manage user profiles with hashed passwords using Argon2.
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc OpenAPI specs.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database / ORM**: SQLite, [SQLAlchemy](https://www.sqlalchemy.org/)
- **Security**: [python-jose](https://github.com/mpdavis/python-jose) (JWT), [argon2-cffi](https://argon2-cffi.readthedocs.io/)
- **Configuration**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## Getting Started

### 1. Clone & Set Up Virtual Environment

```bash
# Clone the repository
git clone <repo-url>
cd fastapi-expense-tracker

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run the Application

```bash
cd app
fastapi dev main.py
# or
uvicorn main:app --reload
```

The database tables will be automatically initialized in `localDB.db`.

## API Documentation

Once the server is running, visit:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### Auth
- `POST /auth/login` - Authenticate and obtain JWT access token

### Users
- `POST /users/` - Register a new user (Public)
- `GET /users/` - List all users *(Protected)*
- `GET /users/{id}` - Get user details by ID *(Protected)*
- `PUT /users/{id}` - Update user details *(Protected)*
- `DELETE /users/{id}` - Delete user *(Protected)*

### Expenses
- `POST /expenses/` - Create a new expense *(Protected)*
- `GET /expenses/` - List all expenses *(Protected)*
- `GET /expenses/search?title={query}` - Search expenses by title *(Protected)*
- `GET /expenses/{id}` - Get expense details by ID *(Protected)*
- `PUT /expenses/{id}` - Update expense by ID *(Protected)*
- `DELETE /expenses/{id}` - Delete expense by ID *(Protected)*
