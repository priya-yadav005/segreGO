# SegreGo - Waste Segregation Tracker

A Django web app for tracking household waste segregation with user authentication, rewards, and leaderboards.

## Features

- User registration and login
- Submit waste entries (Wet/Dry/Mixed)
- View submission history
- Rewards system
- Community leaderboard
- Admin dashboard

## Quick Start

### Setup
```bash
cd "d:\projects\next gen\segrego"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Access
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Usage

**Residents:**
- Register with flat number
- Submit daily waste
- View history and rewards
- Check leaderboard

**Admins:**
- Manage users
- View all submissions
- Monitor waste patterns
- Access dashboard

## Tech Stack

- Python / Django
- SQLite
- HTML / CSS

## Project Structure

```
segrego/
├── waste/              # Main app
│   ├── models.py       # Database models
│   ├── views.py        # Views
│   ├── forms.py        # Forms
│   └── templates/      # HTML templates
├── static/css/         # Styles
├── db.sqlite3          # Database
└── manage.py           # Django CLI
```
- HTML/CSS (server-rendered templates)
