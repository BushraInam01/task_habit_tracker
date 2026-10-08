# Task & Habit Tracker

A Django-based Task & Habit Tracker that helps users manage daily tasks, track habits, monitor streaks, and view weekly progress.

## Features

- Task management
- Task priority and due dates
- Task completion tracking
- Habit management
- Daily habit completion
- Habit streak tracking
- Calendar view for task and habit history
- Weekly summary report
- Weekly summary email
- Dark mode with user profile settings
- HTMX inline task editing
- HTMX habit completion toggle
- Chart.js progress charts
- Celery background tasks
- Celery Beat scheduled tasks
- RabbitMQ message broker
- Django Static Files
- Django Compressor

## Technologies

- Python
- Django
- Django ORM
- ModelForms
- HTMX
- Chart.js
- Celery
- Celery Beat
- RabbitMQ
- Django Compressor
- SQLite

## Project Structure

```text
task_habit_tracker/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
│
├── tracker/
│   ├── migrations/
│   ├── templates/
│   │   └── tracker/
│   ├── static/
│   │   └── tracker/
│   │       ├── css/
│   │       └── js/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tasks.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd task_habit_tracker
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python3 manage.py migrate
```

### 5. Create a Superuser

```bash
python3 manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python3 manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/

## Celery Setup

Celery is used for background tasks such as sending the weekly summary email.

### Start Celery Worker

```bash
celery -A config worker --loglevel=info
```

### Start Celery Beat

```bash
celery -A config beat --loglevel=info
```

RabbitMQ is used as the message broker for Celery.

## Static Files

Static files include CSS and JavaScript used by the application.

Collect static files using:

```bash
python3 manage.py collectstatic
```

The collected files are stored in:

```text
staticfiles/
```

## Django Compressor

Django Compressor is used to process and compress CSS and JavaScript files.

Example:

```django
{% load static %}
{% load compress %}

{% compress css %}
<link rel="stylesheet" href="{% static 'tracker/css/style.css' %}">
{% endcompress %}
```

## Database

The project uses SQLite as the default database during development.

## Learning Objectives

This project was developed to practice and understand:

- Django project and app structure
- Django Models
- Django ORM
- ModelForms
- Function-Based Views
- Custom model methods
- Django signals
- OneToOne relationships
- HTMX
- Inline editing
- Date-based ORM functions
- TruncDay
- ExtractWeekDay
- Celery
- Celery Beat
- RabbitMQ
- Chart.js
- Static files
- Django Compressor

## Project Status

The Task & Habit Tracker project is complete with the required task management, habit tracking, reporting, asynchronous email, HTMX, charting, dark mode, static files, and compression features implemented.