from rest_framework import serializers
from .models import AttendanceRecord

class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_code = serializers.CharField(source='employee.user.employee_id', read_only=True)
    class Meta:
        model = AttendanceRecord
        fields = ('id', 'employee', 'employee_name', 'employee_code', 'date', 'check_in', 'check_out', 'status', 'working_hours', 'remarks', 'created_at', 'updated_at')
        read_only_fields = ('working_hours', 'created_at', 'updated_at')

class CheckInSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)

class CheckOutSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)
