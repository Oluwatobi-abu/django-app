# 🚀 Django Full-Stack App — Fibonacci Generator & Todo List

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)](https://postgresql.org)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render)](https://django-app-1aqk.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-deployed Django web application featuring a mathematically elegant Fibonacci series generator and a fully functional PostgreSQL-backed Todo list — built, tested, and shipped to the cloud.

**🌐 Live Demo:** [https://django-app-1aqk.onrender.com](https://django-app-1aqk.onrender.com)

---

## 📸 Features at a Glance

| Feature | Description |
|---|---|
| 🔢 **Fibonacci Generator** | Generates series up to 1,000 terms using Python's `yield` generator pattern (lazy evaluation) |
| 🔌 **REST-style JSON API** | `/fibonacci/api/?terms=N` returns series, sum, and count as JSON |
| ✅ **Todo CRUD** | Full Create, Read, Update, Delete with PostgreSQL persistence |
| 🎯 **Priority Levels** | Tasks tagged Low / Medium / High with colour-coded indicators |
| 📅 **Due Dates** | Optional due date field per task |
| 🔍 **Filters** | Filter todos by completion status and priority level |
| 🧹 **Bulk Clear** | One-click clear of all completed tasks |
| ⚙️ **Django Admin** | Full admin panel for database management |
| 🚀 **Production Ready** | Deployed with Gunicorn + WhiteNoise + Render + PostgreSQL |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Django 4.2 |
| **Database** | PostgreSQL 17 (via psycopg2) |
| **Web Server** | Gunicorn (production), Django dev server (local) |
| **Static Files** | WhiteNoise (no nginx required) |
| **Deployment** | Render (PaaS) |
| **DB Config** | `dj-database-url` for environment-based DB switching |

---

## 🧠 Technical Highlights

### Fibonacci — Python Generator Pattern

The generator uses Python's `yield` keyword for **lazy evaluation** — values are computed one at a time, never loading the entire sequence into memory at once. This is O(1) space complexity regardless of how many terms are requested.

```python
def fibonacci_generator(n):
    """
    Lazy Fibonacci generator using Python's yield.
    Memory-efficient: produces values on demand, not all at once.
    Time complexity: O(n) | Space complexity: O(1)
    """
    a, b = 0, 1
    count = 0
    while count < n:
        yield a          # suspends here, resumes on next()
        a, b = b, a + b
        count += 1

# Consumed lazily — only computes what's needed
series = list(fibonacci_generator(10))
# → [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### JSON API Endpoint

```bash
GET /fibonacci/api/?terms=10

# Response
{
  "terms": 10,
  "series": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
  "sum": 88,
  "count": 10
}
```

### PostgreSQL Schema

```sql
CREATE TABLE todos (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT         DEFAULT '',
    completed   BOOLEAN      DEFAULT FALSE,
    priority    VARCHAR(10)  DEFAULT 'medium',  -- low | medium | high
    due_date    DATE,
    created_at  TIMESTAMPTZ  NOT NULL,
    updated_at  TIMESTAMPTZ  NOT NULL
);
```

---

## 📁 Project Structure

```
django-app/
├── manage.py                    # Django CLI entry point
├── settings.py                  # Unified local + production config
├── urls.py                      # Root URL dispatcher
├── wsgi.py                      # WSGI entry point (Gunicorn)
├── build.sh                     # Render deploy script
├── requirements.txt
├── .gitignore
│
├── fibonacci/                   # Fibonacci app
│   ├── views.py                 # Generator logic + JSON API
│   ├── urls.py                  # /fibonacci/ routes
│   ├── models.py                # Stateless — no DB needed
│   └── apps.py
│
├── todo/                        # Todo app
│   ├── models.py                # Todo model (PostgreSQL)
│   ├── views.py                 # CRUD views
│   ├── admin.py                 # Django admin registration
│   ├── urls.py                  # /todo/ routes
│   └── migrations/
│       └── 0001_initial.py
│
└── templates/
    ├── fibonacci/
    │   └── index.html
    └── todo/
        ├── index.html
        └── edit.html
```

---

## ⚡ Quick Start (Local)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- pip

### 1. Clone the repo
```bash
git clone https://github.com/Oluwatobi-abu/django-app.git
cd django-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
```sql
-- In psql
CREATE DATABASE django_app;
```

### 4. Configure environment
```bash
# Windows PowerShell
$env:DB_NAME     = "django_app"
$env:DB_USER     = "postgres"
$env:DB_PASSWORD = "your_password"
$env:DB_HOST     = "localhost"
$env:DB_PORT     = "5432"
$env:DEBUG       = "True"
```

### 5. Run migrations & start server
```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000` 🎉

---

## 🌐 Live URLs

| Route | Description |
|---|---|
| [`/`](https://django-app-1aqk.onrender.com/) | Todo List |
| [`/fibonacci/`](https://django-app-1aqk.onrender.com/fibonacci/) | Fibonacci Generator |
| [`/fibonacci/api/?terms=20`](https://django-app-1aqk.onrender.com/fibonacci/api/?terms=20) | JSON API |
| [`/admin/`](https://django-app-1aqk.onrender.com/admin/) | Django Admin Panel |

---

## ☁️ Deployment (Render)

This app is deployed on [Render](https://render.com) using:

- **Web Service** — Python 3, starts with `gunicorn wsgi:application --bind 0.0.0.0:10000`
- **PostgreSQL** — managed Render database, connected via `DATABASE_URL` env var
- **Auto-deploy** — every push to `main` triggers a redeploy via `build.sh`

### `build.sh` (runs on every deploy)
```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Required Environment Variables on Render

| Variable | Description |
|---|---|
| `DATABASE_URL` | Render PostgreSQL internal connection string |
| `SECRET_KEY` | Django secret key (use a long random string) |
| `DEBUG` | Set to `False` in production |

---

## 🔮 Potential Improvements

- [ ] User authentication — personal todo lists per account
- [ ] Django REST Framework — full API layer
- [ ] Task categories and tags
- [ ] Email reminders for due dates
- [ ] Unit tests with `pytest-django`
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Custom domain name

---

## 👤 Author

**Oluwatobi**
- GitHub: [@Oluwatobi-abu](https://github.com/Oluwatobi-abu)
- Live App: [django-app-1aqk.onrender.com](https://django-app-1aqk.onrender.com)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
