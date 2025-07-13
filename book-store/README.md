# Book Store API

This is a FastAPI project for a book store application. It provides a RESTful API to manage books and related data.

## Project Structure

```
book-store
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── models           # Contains data models
│   ├── routes           # Defines API routes
│   ├── schemas          # Pydantic schemas for data validation
│   └── utils            # Utility functions
├── tests                # Contains test cases for the application
│   └── test_main.py     # Unit tests
├── requirements.txt     # Lists project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd book-store
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

Once the application is running, you can access the API at `http://127.0.0.1:8000`. You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Testing

To run the tests, use the following command:
```bash
pytest
```

## License

This project is licensed under the MIT License.