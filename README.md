# CRUD Operations with ChromaDB Vector Database

A Python package that provides CRUD (Create, Read, Update, Delete) operations for text documents using ChromaDB as a vector database backend.

## Features

- Create collections to organize documents
- Insert text documents with automatic UUID generation
- Update existing documents
- Delete documents by ID
- Retrieve similar documents using vector similarity search
- Built-in error handling and input validation

## Installation

```bash
# Clone the repository
git clone https://github.com/maxmoriss/vector_crud.git
cd vector_crud

# Install dependencies
pip install -r requirements.txt
```

## Usage

See [examples/usage.md](examples/usage.md)

### Running Tests

```bash
# Run tests
pytest

# Test coverage
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
vector_crud/vector_db_connector.py      50      0   100%
```

### Running the REST API

```bash
# Start FastAPI uvicorn server
uvicorn vector_crud.api.main:app --reload

# See the API documentation at
http://127.0.0.1:8000/docs
```

### Project Structure

```
vector_crud/
├── vector_crud/
│   ├── __init__.py
│   ├── vector_db_connector.py
│   ├── exceptions.py
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       └── models.py
├── tests/
│   └── test_vector_db_connector.py
├── examples/
│   └── usage.md
├── docs/
├── requirements.txt
└── README.md
```

## Dependencies

- Python 3.8+
- ChromaDB
- FastAPI (for REST API)
- pytest (for testing)
- pytest-mock (for testing)
