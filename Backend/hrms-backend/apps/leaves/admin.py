from django.contrib import admin
from .models import LeaveType, LeaveRequest, LeaveBalance
admin.site.register(LeaveType); admin.site.register(LeaveRequest); admin.site.register(LeaveBalance)
