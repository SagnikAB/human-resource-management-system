# 🏢 HRMS — Human Resource Management System

> **Hackathon-grade, production-ready full-stack HRMS** built with Next.js 14 + Django REST Framework + Supabase PostgreSQL. Dark glassmorphism UI with silky Framer Motion animations.

![Tech Stack](https://img.shields.io/badge/Frontend-Next.js_14-black?logo=next.js)
![Django](https://img.shields.io/badge/Backend-Django_4.2-green?logo=django)
![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 📸 Features at a Glance

| Feature | Employee | Admin/HR |
|---|---|---|
| 🔐 JWT Auth (login/register) | ✅ | ✅ |
| 📊 Animated Dashboard | ✅ | ✅ |
| 👤 Profile Management | View + limited edit | Full edit |
| 📅 Attendance (check-in/out) | Own records | All employees |
| 🌴 Leave Requests | Apply + track | Approve/Reject |
| 💰 Payroll/Salary | Read-only view | Full control |
| 🔔 Role-based Access | ✅ | ✅ |
| 📱 Responsive / Mobile | ✅ | ✅ |

---

## 🗂️ Project Structure

```
hrms/
├── hrms-frontend/          # Next.js 14 App Router (TypeScript)
│   ├── app/
│   │   ├── (auth)/         # Login, Register
│   │   ├── (dashboard)/    # Employee pages
│   │   └── admin/          # Admin pages
│   ├── components/         # Reusable UI components
│   ├── lib/                # API client, auth store, Supabase
│   ├── hooks/              # React Query hooks
│   └── types/              # TypeScript interfaces
│
└── hrms-backend/           # Django REST Framework (Python 3.11)
    ├── apps/
    │   ├── authentication/ # JWT auth, CustomUser
    │   ├── employees/      # Profiles, departments
    │   ├── attendance/     # Check-in/out, records
    │   ├── leaves/         # Leave requests & approvals
    │   └── payroll/        # Salary structure & payslips
    └── hrms/
        └── settings/       # base / development / production
```

---

## ⚡ Quick Start (Local Development)

### Prerequisites
- Node.js 20+
- Python 3.11+
- A [Supabase](https://supabase.com) project (free tier works)

---

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/hrms.git
cd hrms
```

---

### 2. Backend Setup

```bash
cd hrms-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — fill in your Supabase DATABASE_URL and SECRET_KEY
```

**Edit `.env`:**
```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
DJANGO_SETTINGS_MODULE=hrms.settings.development
```

```bash
# Run migrations
python manage.py migrate

# Seed demo data (1 admin + 10 employees)
python manage.py create_demo_data

# Start backend
python manage.py runserver
# API running at: http://localhost:8000/api/
```

**Demo Credentials:**
| Role | Email | Password |
|---|---|---|
| Admin | admin@hrms.com | Admin@123 |
| Employee | employee1@hrms.com | Employee@123 |

---

### 3. Frontend Setup

```bash
cd hrms-frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
```

**Edit `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

```bash
# Start frontend
npm run dev
# App running at: http://localhost:3000
```

---

## 🚀 Production Deployment

### Frontend → Vercel

1. Push `hrms-frontend/` to a GitHub repo
2. Import into [Vercel](https://vercel.com/new)
3. Add Environment Variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` → your backend URL
   - `NEXT_PUBLIC_SUPABASE_URL` → your Supabase URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` → your Supabase anon key
4. Deploy — Vercel auto-deploys on every `git push main`

**GitHub Actions Secrets needed** (for CI/CD):
```
VERCEL_TOKEN          → from vercel.com/account/tokens
VERCEL_ORG_ID         → from vercel.com/account (or team settings)
VERCEL_PROJECT_ID     → from your Vercel project settings
NEXT_PUBLIC_API_URL   → your production backend URL
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
```

---

### Backend → Render (recommended free tier)

1. Push `hrms-backend/` to a GitHub repo
2. Create a new **Web Service** at [render.com](https://render.com)
3. Settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command:** `gunicorn hrms.wsgi:application --bind 0.0.0.0:$PORT`
   - **Python Version:** 3.11
4. Add Environment Variables in Render dashboard:
   ```
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(50))">
   DEBUG=False
   DATABASE_URL=<your Supabase postgres connection string>
   ALLOWED_HOSTS=<your-app>.onrender.com
   CORS_ALLOWED_ORIGINS=https://<your-vercel-app>.vercel.app
   DJANGO_SETTINGS_MODULE=hrms.settings.production
   ```
5. Deploy — auto-deploys on push to `main`

**GitHub Actions Secrets needed:**
```
RENDER_DEPLOY_HOOK_URL  → from Render service settings → "Deploy Hook"
```

---

### Supabase Setup

1. Go to [supabase.com](https://supabase.com) → New Project
2. Note your **Project URL** and **anon public key** (Settings → API)
3. Get **DATABASE_URL** from: Settings → Database → Connection String (URI mode)
   - Use the **Pooler** connection string for production
4. That's it — Django migrations create all tables automatically

---

## 🔌 API Reference

Base URL: `http://localhost:8000/api`

### Authentication
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register/` | Register new user | No |
| POST | `/auth/login/` | Login → returns JWT | No |
| POST | `/auth/token/refresh/` | Refresh access token | Refresh token |
| POST | `/auth/logout/` | Blacklist refresh token | Yes |
| GET | `/auth/me/` | Current user info | Yes |
| POST | `/auth/change-password/` | Change password | Yes |

### Employees
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/employees/` | List all employees | Admin |
| POST | `/employees/` | Create employee | Admin |
| GET | `/employees/me/` | My profile | Employee |
| GET | `/employees/{id}/` | Get profile | Admin/Owner |
| PATCH | `/employees/{id}/` | Update profile | Admin/Owner |
| POST | `/employees/{id}/upload-avatar/` | Upload photo | Admin/Owner |
| GET | `/departments/` | List departments | Admin |

### Attendance
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/attendance/` | List records | Admin/Own |
| POST | `/attendance/check-in/` | Check in | Employee |
| POST | `/attendance/check-out/` | Check out | Employee |
| GET | `/attendance/today/` | Today's record | Employee |
| GET | `/attendance/summary/` | Monthly summary | Employee |

### Leaves
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/leaves/requests/` | List requests | Admin/Own |
| POST | `/leaves/requests/` | Apply for leave | Employee |
| POST | `/leaves/requests/{id}/approve/` | Approve | Admin |
| POST | `/leaves/requests/{id}/reject/` | Reject | Admin |
| GET | `/leaves/balance/` | Leave balance | Employee |
| GET | `/leaves/types/` | Leave types | All |

### Payroll
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/payroll/salary-structure/` | Salary structure | Admin/Own |
| PUT | `/payroll/salary-structure/{id}/` | Update salary | Admin |
| GET | `/payroll/records/` | Payroll records | Admin/Own |
| POST | `/payroll/generate/` | Generate payroll | Admin |

### Dashboard
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET | `/dashboard/stats/` | KPI stats | Admin |
| GET | `/health/` | Health check | No |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                       │
│         Next.js 14 App (Vercel CDN Edge)                │
│  ┌──────────┐  ┌───────────┐  ┌───────────────────┐   │
│  │ Framer   │  │  Zustand  │  │  TanStack Query   │   │
│  │ Motion   │  │ Auth Store│  │  (API Cache)      │   │
│  └──────────┘  └───────────┘  └───────────────────┘   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS (JWT Bearer)
┌──────────────────────▼──────────────────────────────────┐
│              DJANGO REST FRAMEWORK (Render)             │
│  ┌──────────┐  ┌───────────┐  ┌───────────────────┐   │
│  │ JWT Auth │  │ RBAC      │  │  Rate Limiting    │   │
│  │ SimpleJWT│  │ Permissions│  │  (django-ratelimit)│  │
│  └──────────┘  └───────────┘  └───────────────────┘   │
│  Apps: auth | employees | attendance | leaves | payroll │
└──────────────────────┬──────────────────────────────────┘
                       │ PostgreSQL (SSL)
┌──────────────────────▼──────────────────────────────────┐
│                  SUPABASE (PostgreSQL)                  │
│  Tables: users | employee_profiles | departments |      │
│          attendance_records | leave_requests |          │
│          leave_balances | salary_structures |           │
│          payroll_records | leave_types                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔒 Security Features

- **JWT Authentication** — 15-min access tokens, 7-day refresh tokens with blacklisting
- **Role-Based Access Control** — Admin/HR vs Employee permissions at API level
- **Rate Limiting** — 5 login attempts per IP per minute
- **Password Policy** — min 8 chars, uppercase + digit + special char required
- **CORS** — whitelist-only, configured per environment
- **Security Headers** — HSTS, X-Frame-Options, XSS Protection, CSP (via Vercel)
- **Input Validation** — strict DRF serializer validation on all endpoints
- **SQL Injection** — ORM-only, zero raw queries
- **HTTPS Enforced** — production settings redirect HTTP → HTTPS
- **SAST** — Bandit runs on every CI push

---

## 🎨 Design System

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#0a0a0f` | Page background |
| `--surface` | `#13131a` | Cards, panels |
| `--border` | `#1e1e2e` | Dividers, outlines |
| `--accent` | `#7c3aed` | Primary CTA, active states |
| `--accent-2` | `#06b6d4` | Secondary, charts |
| `--success` | `#10b981` | Present, approved |
| `--warning` | `#f59e0b` | Half-day, pending |
| `--danger` | `#ef4444` | Absent, rejected |
| `--text` | `#f1f5f9` | Primary text |
| `--muted` | `#64748b` | Secondary text |

---

## 🧪 Running Tests

```bash
# Backend
cd hrms-backend
python manage.py test

# Frontend (if test suite added)
cd hrms-frontend
npm test
```

---

## 📦 Tech Stack Summary

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + custom design tokens
- **Animations**: Framer Motion
- **Components**: shadcn/ui
- **State**: Zustand (auth) + TanStack Query v5 (server state)
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **HTTP**: Axios

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Auth**: djangorestframework-simplejwt
- **DB**: PostgreSQL via Supabase
- **ORM**: Django ORM
- **CORS**: django-cors-headers
- **Rate limit**: django-ratelimit
- **Server**: Gunicorn + Whitenoise

### Infrastructure
- **Frontend hosting**: Vercel (Edge CDN)
- **Backend hosting**: Render (or Railway)
- **Database**: Supabase (managed PostgreSQL)
- **CI/CD**: GitHub Actions
- **Assets**: Supabase Storage (or Cloudinary)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>Built with ❤️ for Odoo Hackathon</strong><br>
  Every workday, perfectly aligned.
</div>
