from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'employee_id', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'employee_id')
    fieldsets = ((None, {'fields': ('email', 'password')}), ('Profile', {'fields': ('employee_id', 'role')}), ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'date_joined')}))
    readonly_fields = ('employee_id', 'date_joined')
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'role', 'password1', 'password2')}),)
