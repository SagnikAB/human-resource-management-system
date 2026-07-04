from calendar import monthrange
from decimal import Decimal
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdminOrHR
from apps.attendance.models import AttendanceRecord
from apps.employees.models import EmployeeProfile
from .models import SalaryStructure, PayrollRecord
from .serializers import SalaryStructureSerializer, PayrollRecordSerializer, GeneratePayrollSerializer

class SalaryStructureListView(generics.ListAPIView):
    serializer_class = SalaryStructureSerializer
    def get_queryset(self):
        qs = SalaryStructure.objects.select_related('employee', 'updated_by')
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=self.request.user)
        return qs

class SalaryStructureDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SalaryStructureSerializer
    lookup_url_kwarg = 'employee_id'
    def get_queryset(self):
        qs = SalaryStructure.objects.select_related('employee', 'updated_by')
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=self.request.user)
        return qs
    def get_object(self):
        return generics.get_object_or_404(self.get_queryset(), employee__id=self.kwargs['employee_id'])
    def put(self, request, *args, **kwargs):
        if not request.user.is_admin_or_hr:
            return Response({'detail': 'Only admin or HR can update salary structures.'}, status=status.HTTP_403_FORBIDDEN)
        employee = generics.get_object_or_404(EmployeeProfile, id=kwargs['employee_id'])
        obj, _ = SalaryStructure.objects.get_or_create(employee=employee, defaults={'basic_salary': 0, 'effective_from': request.data.get('effective_from'), 'updated_by': request.user})
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True); serializer.save(updated_by=request.user)
        return Response(serializer.data)

class PayrollRecordListView(generics.ListAPIView):
    serializer_class = PayrollRecordSerializer
    def get_queryset(self):
        qs = PayrollRecord.objects.select_related('employee')
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=self.request.user)
        month = self.request.query_params.get('month'); year = self.request.query_params.get('year')
        if month: qs = qs.filter(month=month)
        if year: qs = qs.filter(year=year)
        return qs

class PayrollRecordDetailView(generics.RetrieveAPIView):
    serializer_class = PayrollRecordSerializer
    def get_queryset(self):
        qs = PayrollRecord.objects.select_related('employee')
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=self.request.user)
        return qs

class GeneratePayrollView(APIView):
    permission_classes = [IsAdminOrHR]
    def post(self, request):
        serializer = GeneratePayrollSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        month = serializer.validated_data['month']; year = serializer.validated_data['year']; total_days = monthrange(year, month)[1]
        created = []
        for structure in SalaryStructure.objects.select_related('employee').all():
            attendance = AttendanceRecord.objects.filter(employee=structure.employee, date__month=month, date__year=year)
            present = attendance.filter(status__in=['present', 'half_day']).count()
            absent = max(total_days - present, 0)
            gross = structure.gross_salary
            deductions = structure.total_deductions
            net = gross - deductions
            record, _ = PayrollRecord.objects.update_or_create(employee=structure.employee, month=month, year=year, defaults={'gross_salary': gross, 'total_deductions': deductions, 'net_salary': net, 'days_worked': present, 'days_absent': absent})
            created.append(record)
        return Response(PayrollRecordSerializer(created, many=True).data, status=status.HTTP_201_CREATED)
