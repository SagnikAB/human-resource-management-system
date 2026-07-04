from datetime import date, timedelta, time
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from apps.employees.models import Department, EmployeeProfile
from apps.attendance.models import AttendanceRecord
from apps.leaves.models import LeaveType, LeaveBalance
from apps.payroll.models import SalaryStructure

class Command(BaseCommand):
    help = 'Seed the database with HRMS demo data.'

    def handle(self, *args, **options):
        admin, _ = CustomUser.objects.get_or_create(email='admin@hrms.com', defaults={'role': 'admin', 'is_staff': True, 'is_superuser': True})
        admin.set_password('Admin@123'); admin.save()
        hr_dept, _ = Department.objects.get_or_create(name='Human Resources', defaults={'description': 'People operations and employee success'})
        eng_dept, _ = Department.objects.get_or_create(name='Engineering', defaults={'description': 'Product engineering and infrastructure'})
        leave_types = []
        for name, days, paid in [('Paid', 18, True), ('Sick', 10, True), ('Unpaid', 30, False)]:
            leave_types.append(LeaveType.objects.get_or_create(name=name, defaults={'max_days_per_year': days, 'is_paid': paid})[0])
        employees = []
        for i in range(1, 11):
            user, created = CustomUser.objects.get_or_create(email=f'employee{i}@hrms.com', defaults={'role': 'employee'})
            if created: user.set_password('Employee@123'); user.save()
            profile, _ = EmployeeProfile.objects.get_or_create(user=user, defaults={'first_name': f'Employee{i}', 'last_name': 'Demo', 'phone': f'+100000000{i}', 'city': 'Remote', 'country': 'Global', 'department': eng_dept if i % 2 else hr_dept, 'designation': 'Software Engineer' if i % 2 else 'HR Associate', 'date_of_joining': date.today() - timedelta(days=365+i), 'employment_type': 'full_time', 'bank_name': 'Demo Bank'})
            profile.set_bank_account_number(f'000111222{i}'); profile.save()
            employees.append(profile)
        hr_dept.head = employees[1]; eng_dept.head = employees[0]; hr_dept.save(); eng_dept.save()
        for employee in employees:
            for lt in leave_types:
                LeaveBalance.objects.get_or_create(employee=employee, leave_type=lt, year=date.today().year, defaults={'allocated_days': lt.max_days_per_year})
            SalaryStructure.objects.get_or_create(employee=employee, defaults={'basic_salary': Decimal('50000.00'), 'hra': Decimal('12000.00'), 'transport_allowance': Decimal('3000.00'), 'medical_allowance': Decimal('2000.00'), 'other_allowances': Decimal('5000.00'), 'pf_deduction': Decimal('6000.00'), 'tax_deduction': Decimal('4000.00'), 'other_deductions': Decimal('1000.00'), 'effective_from': date.today() - timedelta(days=180), 'updated_by': admin})
            for d in range(30):
                day = date.today() - timedelta(days=d)
                if day.weekday() >= 5:
                    status = 'weekend'; check_in = check_out = None
                elif d % 11 == 0:
                    status = 'absent'; check_in = check_out = None
                else:
                    status = 'present'; check_in = time(9, 0); check_out = time(17, 30)
                AttendanceRecord.objects.get_or_create(employee=employee, date=day, defaults={'check_in': check_in, 'check_out': check_out, 'status': status})
        self.stdout.write(self.style.SUCCESS('Demo data created: admin@hrms.com / Admin@123 plus 10 employees.'))
