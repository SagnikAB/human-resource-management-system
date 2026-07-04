from rest_framework.permissions import BasePermission

from .models import Employee


def role_for(user):
    if not user or not user.is_authenticated:
        return None
    try:
        return user.employee_profile.role
    except Employee.DoesNotExist:
        return None


def is_hr_user(user):
    return role_for(user) in {Employee.Role.ADMIN, Employee.Role.HR}


class IsHrUser(BasePermission):
    def has_permission(self, request, view):
        return is_hr_user(request.user)
