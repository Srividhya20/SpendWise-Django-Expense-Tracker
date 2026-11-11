# SpendWise — Personal Expense Tracker (Django)

This project is arranged so you can learn Django step by step. The project files are directly inside this folder (no extra nested project folder).

## Before starting
Open this `SpendWise_Beginner_Project` folder in VS Code. Open Terminal > New Terminal.
Your terminal path should end with `SpendWise_Beginner_Project`.

## Windows setup
Run these commands one at a time:

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\Scripts\Activate.ps1
```

## Learn while building — 4-hour route

### Lesson 1 — Django project and app (20 minutes)
- `manage.py`: command-line entry point for Django.
- `config/settings.py`: project configuration.
- `config/urls.py`: main URL routing.
- `tracker/`: our app, where the expense tracker features live.

### Lesson 2 — Models and database (40 minutes)
Open `tracker/models.py`.
- `Category`: expense category such as Food or Transport.
- `Expense`: one expense record owned by a user.
- `MonthlyBudget`: one monthly budget per user.
Run `makemigrations` to create migration instructions, then `migrate` to create database tables.

### Lesson 3 — URLs and views (40 minutes)
Open `tracker/urls.py` and `tracker/views.py`.
A URL chooses a view; the view reads/writes data and returns an HTML template.

### Lesson 4 — Forms and templates (40 minutes)
Open `tracker/forms.py` and `templates/`.
ModelForms create HTML forms from models and validate submitted data.

### Lesson 5 — Test the features (60 minutes)
1. Register an account.
2. Add an expense.
3. Edit and delete an expense.
4. Set this month's budget.
5. Check the dashboard totals.
6. Register a second account and verify that each user sees only their own expenses.

### Lesson 6 — Interview explanation (20 minutes)
Explain the flow:
Browser URL → `tracker/urls.py` → view in `tracker/views.py` → model/ORM → template → HTML response.

## Important Django commands
```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Features
- Registration, login and logout
- User-specific expenses
- Add, view, edit and delete expenses
- Default expense categories
- Monthly budget
- Dashboard with monthly totals and category breakdown

SQLite is used by default; you do not need to install MySQL to run this version.
This is a learning/demo project. Do not deploy with `DEBUG=True` or the sample secret key.
