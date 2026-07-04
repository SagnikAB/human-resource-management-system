# Human Resource Management System

This repository contains a GitHub Pages-ready HRMS website and a Django REST backend.

## Static Website

The static website is deployed from the repository root:

- `index.html`
- `styles.css`
- `app.js`
- `wireframe-reference.jpeg`

Demo accounts:

- Admin: `admin@company.test` / `AdminPass123!`
- Employee: `alex.employee@company.test` / `EmployeePass123!`

The GitHub Pages prototype stores demo interactions in browser `localStorage`, so profile edits, attendance check-ins, leave requests, and salary edits persist in the same browser.

## GitHub Pages Deployment

1. Push this repository to GitHub.
2. Open repository `Settings`.
3. Go to `Pages`.
4. Use either:
   - Source: `GitHub Actions`, or
   - Source: `Deploy from a branch`, branch `main`, folder `/ (root)`.
5. Save.

The Pages URL will be:

```text
https://sagnikab.github.io/human-resource-management-system/
```

## Django Backend

The backend lives in `backend/` and provides REST APIs for authentication, employees, attendance, leave requests, salary structures, and payroll.

### Local Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

The API runs at:

```text
http://127.0.0.1:8000/api/
```

### Demo Backend Accounts

- Admin: `admin@company.test` / `AdminPass123!`
- Employee: `alex.employee@company.test` / `EmployeePass123!`

### Main API Routes

- `POST /api/auth/signup/`
- `POST /api/auth/signin/`
- `GET /api/employees/`
- `GET /api/employees/me/`
- `POST /api/attendance/check-in/`
- `POST /api/attendance/check-out/`
- `GET /api/leave-requests/`
- `PATCH /api/leave-requests/:id/decision/`
- `GET /api/payroll/`
- `POST /api/salary-structures/`

Protected endpoints use DRF token authentication:

```text
Authorization: Token <token>
```

## Backend Deployment

`render.yaml` is included for deploying the Django API to Render.

On Render:

1. Create a new Blueprint.
2. Connect this GitHub repo.
3. Render will detect `render.yaml`.
4. Add a PostgreSQL database and set `DATABASE_URL` if you want production persistence.
5. After deploy, run:

```bash
python manage.py seed_demo
```
