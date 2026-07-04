from rest_framework import serializers
from .models import SalaryStructure, PayrollRecord

class SalaryStructureSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    gross_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_deductions = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = SalaryStructure
        fields = ('id', 'employee', 'employee_name', 'basic_salary', 'hra', 'transport_allowance', 'medical_allowance', 'other_allowances', 'pf_deduction', 'tax_deduction', 'other_deductions', 'gross_salary', 'total_deductions', 'effective_from', 'updated_by', 'updated_at')
        read_only_fields = ('updated_by', 'updated_at')

class PayrollRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    class Meta:
        model = PayrollRecord
        fields = '__all__'
        read_only_fields = ('generated_at',)

class GeneratePayrollSerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=2000, max_value=2100)
