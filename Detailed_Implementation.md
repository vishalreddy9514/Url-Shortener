# URL Shortener Service

A simple in‑memory URL shortening service built with Flask. This project supports:

- ``: Shorten a long URL and return a 6‑character code.
- ``: Redirect to the original URL and increment click count.
- ``: Retrieve the original URL, click count, and creation timestamp.
- **Health checks**:
  - `GET /` → `{ status: "healthy", service: "URL Shortener API" }`
  - `GET /api/health` → `{ status: "ok", message: "URL Shortener API is running" }`

---

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py      # Package marker
│   ├── main.py          # Flask app and routes
│   ├── models.py        # In-memory store with thread lock
│   └── utils.py         # URL validation & code generation
├── tests/
│   └── test_basic.py    # pytest suite (7 tests)
├── requirements.txt
├── README.md            # (this file)
└── NOTES.md (optional)  # Implementation notes
```

---

## Installation

1. Clone or download this repository.
2. Navigate into the project folder:
   ```bash
   cd url-shortener
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running Tests

Before running, ensure `app/` is importable. 

set `PYTHONPATH` manually:

  ```bash
  export PYTHONPATH=$(pwd)
  ```

Then run:

```bash
pytest -q
```

All **7 tests** should pass with no warnings.

---

## Running the Service

1. Set the Flask app environment variable:
   ```bash
   export FLASK_APP=app.main
   ```
2. Start the development server:
   ```bash
   flask run
   # or: python -m flask --app app.main run
   ```
3. The API is now available at `http://localhost:5000`.

### Sanity‑Check with `curl`

- **Shorten a URL**:

  ```bash
  curl -X POST http://localhost:5000/api/shorten \
       -H "Content-Type: application/json" \
       -d '{"url":"https://example.com/long/path"}'
  ```

- **Check redirect headers**:

  ```bash
  curl -I http://localhost:5000/<short_code>
  ```

- **Follow the redirect**:

  ```bash
  curl -L http://localhost:5000/<short_code>
  ```

- **Fetch analytics**:

  ```bash
  curl http://localhost:5000/api/stats/<short_code>
  ```

---

## Design Decisions

- **In‑memory dict + **`` for thread‑safe storage without an external database.
- `` for minimal URL validation (HTTP/HTTPS and netloc only).
- `` for cryptographically secure, 6‑character alphanumeric codes.
- **Error handling**:
  - 400 Bad Request for missing/invalid JSON or URLs
  - 404 Not Found for unknown short codes
- No custom codes, no rate limiting, no authentication, no external DB—keeping it simple.

---

