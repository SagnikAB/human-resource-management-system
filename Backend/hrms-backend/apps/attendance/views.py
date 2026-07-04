from datetime import date
from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdminOrHR, IsOwnerOrAdmin
from apps.employees.models import EmployeeProfile
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer, CheckInSerializer, CheckOutSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    filterset_fields = ('employee', 'date', 'status')
    ordering_fields = ('date', 'created_at')

    def get_queryset(self):
        qs = AttendanceRecord.objects.select_related('employee', 'employee__user')
        user = self.request.user
        if not user.is_admin_or_hr:
            qs = qs.filter(employee__user=user)
        employee_id = self.request.query_params.get('employee_id')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if employee_id: qs = qs.filter(employee__user__employee_id=employee_id)
        if month: qs = qs.filter(date__month=month)
        if year: qs = qs.filter(date__year=year)
        return qs

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy']:
            return [IsAdminOrHR()]
        return [IsOwnerOrAdmin()]

    @action(detail=False, methods=['post'], url_path='check-in')
    def check_in(self, request):
        serializer = CheckInSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        employee = generics.get_object_or_404(EmployeeProfile, user=request.user, is_deleted=False)
        record, created = AttendanceRecord.objects.get_or_create(employee=employee, date=date.today(), defaults={'check_in': timezone.localtime().time(), 'status': 'present', 'remarks': serializer.validated_data.get('remarks', '')})
        if not created and record.check_in:
            return Response({'detail': 'Already checked in today.'}, status=status.HTTP_400_BAD_REQUEST)
        if not created:
            record.check_in = timezone.localtime().time(); record.status = 'present'; record.save()
        return Response(AttendanceRecordSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='check-out')
    def check_out(self, request):
        serializer = CheckOutSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        employee = generics.get_object_or_404(EmployeeProfile, user=request.user, is_deleted=False)
        record = generics.get_object_or_404(AttendanceRecord, employee=employee, date=date.today())
        if record.check_out:
            return Response({'detail': 'Already checked out today.'}, status=status.HTTP_400_BAD_REQUEST)
        record.check_out = timezone.localtime().time()
        if serializer.validated_data.get('remarks'):
            record.remarks = serializer.validated_data['remarks']
        record.save()
        return Response(AttendanceRecordSerializer(record).data)

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        employee = generics.get_object_or_404(EmployeeProfile, user=request.user, is_deleted=False)
        record = AttendanceRecord.objects.filter(employee=employee, date=date.today()).first()
        return Response(AttendanceRecordSerializer(record).data if record else {})

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        qs = self.get_queryset()
        month = request.query_params.get('month', date.today().month)
        year = request.query_params.get('year', date.today().year)
        rows = qs.filter(date__month=month, date__year=year).values('status').annotate(count=Count('id'))
        data = {row['status']: row['count'] for row in rows}
        return Response({'month': int(month), 'year': int(year), 'summary': data})

class EmployeeAttendanceView(APIView):
    permission_classes = [IsAdminOrHR]
    def get(self, request, employee_id):
        qs = AttendanceRecord.objects.filter(employee__id=employee_id).order_by('-date')
        return Response(AttendanceRecordSerializer(qs, many=True).data)
