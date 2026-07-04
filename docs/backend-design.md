# HRMS Django Backend Design

## Product Scope

The Django backend supports:

- Token-based sign up and sign in.
- Role-based access for `ADMIN`, `HR`, and `EMPLOYEE`.
- Employee profile management.
- Attendance check-in/check-out and attendance history.
- Leave request creation, approval, rejection, and audit logging.
- Salary structure management and read-only employee payroll visibility.

## Stack

- Django 5
- Django REST Framework
- DRF token authentication
- SQLite for local development
- PostgreSQL-compatible `DATABASE_URL` support for deployment
- WhiteNoise for static file serving on Python hosts
- Render Blueprint config in `render.yaml`

## Data Model

- `Employee`: one-to-one profile linked to Django `User`.
- `EmployeeDocument`: profile document metadata.
- `AttendanceRecord`: one employee attendance record per work date.
- `LeaveRequest`: employee time-off workflow.
- `LeaveBalance`: annual leave allocation and usage.
- `SalaryStructure`: active and historical salary structure records.
- `PayrollRecord`: monthly payroll records.
- `AuditLog`: admin/HR workflow history.

## API Rules

- Employees can read and update only limited profile fields via `/api/employees/me/`.
- Admin/HR users can list and update employee records.
- Employees can only see their own attendance, leave, and published payroll records.
- Admin/HR users can see all attendance, leave, salary, and payroll records.
- Leave decisions are restricted to Admin/HR users.
- Creating a new salary structure marks the employee's previous active structure inactive.

## Auth

`POST /api/auth/signin/` returns a DRF token.

Use it as:

```text
Authorization: Token <token>
```
