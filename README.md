# Personal Expense Tracker

A Django-based web application for tracking personal expenses with REST API support and PostgreSQL database.

## Features

- Django REST Framework (DRF) backend
- PostgreSQL database hosted on Render
- User authentication and authorization
- CRUD operations for expenses
- Django Templates for frontend
- CORS support for API access

## Tech Stack

- Python 3.x
- Django 4.2.7
- Django REST Framework
- PostgreSQL
- Django Templates

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/JacklineMacharia/Personal_Expense_Tracker.git
cd Personal_Expense_Tracker
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Environment Variables

The project uses the following environment variables:
- `DATABASE_URL`: PostgreSQL database URL (configured for Render)

## License

MIT License 