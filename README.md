# Human Resource Management System

A full-stack HRMS with a **GitHub Pages demo** and a **Django REST API** backend.

**Live demo:** [https://sagnikab.github.io/human-resource-management-system/](https://sagnikab.github.io/human-resource-management-system/)

## Features

- Role-based dashboards for **Admin/HR** and **Employees**
- Employee directory with search
- Attendance check-in/out and monthly calendar
- Leave requests with HR approval workflow
- Payroll and salary structure management
- Responsive layout with mobile navigation
- Demo data persisted in browser `localStorage`

## Demo Accounts

| Role     | Email                         | Password           |
|----------|-------------------------------|--------------------|
| Admin    | `admin@company.test`          | `AdminPass123!`    |
| Employee | `alex.employee@company.test`  | `EmployeePass123!` |

Use **Reset Demo** in the sidebar to restore seed data after experimenting.

## Static Website (GitHub Pages)

The static site is deployed automatically via GitHub Actions on every push to `main`.

Manual setup (if needed):

1. Open repository **Settings → Pages**
2. Set **Source** to **GitHub Actions**
3. Push to `main` — the workflow in `.github/workflows/pages.yml` handles the rest

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

API base URL: `http://127.0.0.1:8000/api/`

### Main API Routes

| Method | Route |
|--------|-------|
| POST | `/api/auth/signup/` |
| POST | `/api/auth/signin/` |
| GET | `/api/employees/` |
| GET/PATCH | `/api/employees/me/` |
| POST | `/api/attendance/check-in/` |
| POST | `/api/attendance/check-out/` |
| GET | `/api/leave-requests/` |
| PATCH | `/api/leave-requests/:id/decision/` |
| GET | `/api/payroll/` |
| POST | `/api/salary-structures/` |

Protected endpoints use token authentication:

```text
Authorization: Token <token>
```

## Backend Deployment (Render)

`render.yaml` is included for deploying the Django API to [Render](https://render.com).

1. Create a new **Blueprint** and connect this GitHub repo
2. Render detects `render.yaml` automatically
3. Add a PostgreSQL database and set `DATABASE_URL` for production persistence
4. After deploy, run `python manage.py seed_demo`

## Repository Structure

```text
├── index.html          # Static site entry
├── app.js              # Demo SPA logic
├── styles.css          # UI styles
├── wireframe-reference.svg
├── backend/            # Django REST API
├── render.yaml         # Render deployment config
└── .github/workflows/  # GitHub Pages CI
```
