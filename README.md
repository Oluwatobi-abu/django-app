# Django App: Fibonacci Generator + Todo List

## Features
- **Fibonacci Generator** — uses Python's `yield` generator pattern, lazy evaluation, supports up to 1000 terms, JSON API endpoint
- **Todo List** — full CRUD backed by PostgreSQL, priority levels (low/medium/high), due dates, filter by status & priority, clear completed

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create PostgreSQL database
```sql
CREATE DATABASE django_app;
```

### 3. Configure environment variables (optional, defaults shown)
```bash
export DB_NAME=django_app
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

### 4. Run migrations
```bash
cd django_project
python manage.py migrate
```

### 5. Start the server
```bash
python manage.py runserver
```

---

## URLs

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Todo List |
| `http://localhost:8000/fibonacci/` | Fibonacci Generator |
| `http://localhost:8000/fibonacci/api/?terms=20` | Fibonacci JSON API |
| `http://localhost:8000/admin/` | Django Admin |

---

## Project Structure

```
django_project/
├── settings.py          # Django configuration
├── urls.py              # Root URL config
├── manage.py            # Django management CLI
├── requirements.txt
├── fibonacci/
│   ├── views.py         # Generator logic + views
│   └── urls.py
└── todo/
    ├── models.py        # Todo model (PostgreSQL)
    ├── views.py         # CRUD views
    ├── urls.py
    └── migrations/
        └── 0001_initial.py
```

---

## Fibonacci Generator — How it works

```python
def fibonacci_generator(n):
    """Python generator using yield — lazy evaluation."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a          # Yields one value at a time
        a, b = b, a + b
        count += 1

# Usage
series = list(fibonacci_generator(10))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Todo Model Schema (PostgreSQL)

```sql
CREATE TABLE todos (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    completed   BOOLEAN DEFAULT FALSE,
    priority    VARCHAR(10) DEFAULT 'medium',  -- low | medium | high
    due_date    DATE,
    created_at  TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL
);
```
