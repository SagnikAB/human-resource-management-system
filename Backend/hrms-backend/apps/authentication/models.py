import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _generate_employee_id(self):
        while True:
            employee_id = f"EMP-{random.randint(10000, 99999)}"
            if not self.model.objects.filter(employee_id=employee_id).exists():
                return employee_id

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        extra_fields.setdefault('employee_id', self._generate_employee_id())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        EMPLOYEE = 'employee', 'Employee'
        ADMIN = 'admin', 'Admin'
        HR = 'hr', 'HR Officer'

    employee_id = models.CharField(max_length=16, unique=True, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = CustomUser.objects._generate_employee_id()
        if self.role in [self.Role.ADMIN, self.Role.HR]:
            self.is_staff = True
        super().save(*args, **kwargs)

    @property
    def is_admin_or_hr(self):
        return self.role in [self.Role.ADMIN, self.Role.HR] or self.is_superuser

    def __str__(self):
        return f'{self.email} ({self.employee_id})'
