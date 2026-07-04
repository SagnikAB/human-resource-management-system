from decimal import Decimal
from django.db import models
from apps.employees.models import EmployeeProfile

class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        HALF_DAY = 'half_day', 'Half Day'
        LEAVE = 'leave', 'Leave'
        HOLIDAY = 'holiday', 'Holiday'
        WEEKEND = 'weekend', 'Weekend'

    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            delta = (self.check_out.hour * 60 + self.check_out.minute) - (self.check_in.hour * 60 + self.check_in.minute)
            self.working_hours = Decimal(max(delta, 0)) / Decimal(60)
            if self.working_hours < Decimal('4.00'):
                self.status = self.Status.HALF_DAY
            elif self.status not in [self.Status.LEAVE, self.Status.HOLIDAY, self.Status.WEEKEND]:
                self.status = self.Status.PRESENT
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee} - {self.date} - {self.status}'
