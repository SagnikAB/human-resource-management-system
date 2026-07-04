from django.contrib import admin

from .models import (
    AttendanceRecord,
    AuditLog,
    Employee,
    EmployeeDocument,
    LeaveBalance,
    LeaveRequest,
    PayrollRecord,
    SalaryStructure,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_code", "full_name", "role", "department", "employment_status")
    search_fields = ("employee_code", "first_name", "last_name", "user__email")
    list_filter = ("role", "employment_status", "department")


admin.site.register(EmployeeDocument)
admin.site.register(AttendanceRecord)
admin.site.register(LeaveRequest)
admin.site.register(LeaveBalance)
admin.site.register(SalaryStructure)
admin.site.register(PayrollRecord)
admin.site.register(AuditLog)
