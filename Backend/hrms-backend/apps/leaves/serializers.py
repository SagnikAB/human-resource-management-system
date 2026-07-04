from rest_framework import serializers
from .models import LeaveType, LeaveRequest, LeaveBalance

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    reviewed_by_email = serializers.CharField(source='reviewed_by.email', read_only=True)
    class Meta:
        model = LeaveRequest
        fields = ('id', 'employee', 'employee_name', 'leave_type', 'leave_type_name', 'start_date', 'end_date', 'total_days', 'status', 'reason', 'admin_comment', 'reviewed_by', 'reviewed_by_email', 'reviewed_at', 'created_at')
        read_only_fields = ('employee', 'total_days', 'reviewed_by', 'reviewed_at', 'created_at')

    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('end_date') and attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError('End date cannot be earlier than start date.')
        return attrs

class LeaveBalanceSerializer(serializers.ModelSerializer):
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)
    class Meta:
        model = LeaveBalance
        fields = ('id', 'employee', 'leave_type', 'leave_type_name', 'year', 'allocated_days', 'used_days', 'remaining_days')
