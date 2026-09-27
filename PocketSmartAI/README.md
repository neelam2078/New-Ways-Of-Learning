# PocketSmart AI

PocketSmart AI is a budget-aware generative AI planning application.

It provides three main planners:

1. Home Interior Planner
2. Party Budget Planner
3. Jewelry Planner

The application uses:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- HTML/CSS/JavaScript
- JWT authentication
- Google Gemini
- Pillow
- Pytest

---

# Project Structure

```text
pocketsmart_ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── recommendations.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   ├── recommendation_service.py
│   │   └── catalog_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── home_planner.html
│   │   ├── party_planner.html
│   │   ├── jewelry_planner.html
│   │   └── recommendations.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   └── test_services.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py