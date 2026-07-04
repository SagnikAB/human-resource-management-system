from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hrms.models import Employee, LeaveBalance, PayrollRecord, SalaryStructure

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo HRMS users and records."

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(
            username="admin@company.test",
            defaults={"email": "admin@company.test", "is_staff": True, "is_superuser": True},
        )
        admin_user.email = "admin@company.test"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password("AdminPass123!")
        admin_user.save()

        admin_employee, _ = Employee.objects.get_or_create(
            user=admin_user,
            defaults={
                "employee_code": "HR-001",
                "role": Employee.Role.ADMIN,
                "first_name": "Morgan",
                "last_name": "Admin",
                "department": "Human Resources",
                "designation": "HR Manager",
                "joining_date": "2024-01-15",
            },
        )
        admin_employee.role = Employee.Role.ADMIN
        admin_employee.save()

        employee_user, _ = User.objects.get_or_create(
            username="alex.employee@company.test",
            defaults={"email": "alex.employee@company.test"},
        )
        employee_user.email = "alex.employee@company.test"
        employee_user.set_password("EmployeePass123!")
        employee_user.save()

        employee, _ = Employee.objects.get_or_create(
            user=employee_user,
            defaults={
                "employee_code": "EMP-1001",
                "role": Employee.Role.EMPLOYEE,
                "first_name": "Alex",
                "last_name": "Rivera",
                "department": "Engineering",
                "designation": "Software Engineer",
                "joining_date": "2024-03-04",
            },
        )

        SalaryStructure.objects.get_or_create(
            employee=employee,
            effective_from="2026-01-01",
            defaults={
                "base_salary": Decimal("80000.00"),
                "hra": Decimal("12000.00"),
                "allowances": Decimal("8000.00"),
                "deductions": Decimal("3000.00"),
                "is_active": True,
            },
        )
        LeaveBalance.objects.get_or_create(
            employee=employee,
            leave_type="PAID",
            year=2026,
            defaults={"allocated": Decimal("18.00"), "used": Decimal("0.00")},
        )
        PayrollRecord.objects.get_or_create(
            employee=employee,
            year=2026,
            month=6,
            defaults={
                "gross_pay": Decimal("100000.00"),
                "deductions": Decimal("8500.00"),
                "net_pay": Decimal("91500.00"),
                "published_at": timezone.now(),
            },
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo HRMS data."))
