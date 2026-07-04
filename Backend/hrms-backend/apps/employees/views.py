from datetime import date, timedelta
from django.db.models import Count
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdminOrHR, IsOwnerOrAdmin
from apps.attendance.models import AttendanceRecord
from apps.leaves.models import LeaveRequest
from .models import Department, EmployeeProfile
from .serializers import DepartmentSerializer, EmployeeProfileSerializer, EmployeeProfileListSerializer, AvatarUploadSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    filterset_fields = ('name',)
    search_fields = ('name', 'description')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsOwnerOrAdmin()]
        return [IsAdminOrHR()]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.select_related('user', 'department', 'manager').filter(is_deleted=False)
    permission_classes = [IsOwnerOrAdmin]
    filterset_fields = ('department', 'employment_type', 'gender', 'city', 'country')
    search_fields = ('first_name', 'last_name', 'user__email', 'user__employee_id', 'designation')
    ordering_fields = ('first_name', 'last_name', 'date_of_joining', 'created_at')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeProfileListSerializer
        if self.action == 'upload_avatar':
            return AvatarUploadSerializer
        return EmployeeProfileSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.user.is_active = False
        instance.user.save(update_fields=['is_active'])
        instance.save(update_fields=['is_deleted'])

    def create(self, request, *args, **kwargs):
        if not request.user.is_admin_or_hr:
            return Response({'detail': 'Only admin or HR can create employees.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        profile = generics.get_object_or_404(EmployeeProfile, user=request.user, is_deleted=False)
        return Response(EmployeeProfileSerializer(profile, context={'request': request}).data)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser], url_path='upload-avatar')
    def upload_avatar(self, request, pk=None):
        profile = self.get_object()
        serializer = AvatarUploadSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DashboardStatsView(APIView):
    permission_classes = [IsAdminOrHR]
    def get(self, request):
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        total_employees = EmployeeProfile.objects.filter(is_deleted=False).count()
        present_today = AttendanceRecord.objects.filter(date=today, status='present').count()
        on_leave_today = LeaveRequest.objects.filter(status='approved', start_date__lte=today, end_date__gte=today).count()
        pending_leave_requests = LeaveRequest.objects.filter(status='pending').count()
        week_records = AttendanceRecord.objects.filter(date__gte=week_start, date__lte=today)
        total_week = week_records.count()
        present_week = week_records.filter(status='present').count()
        attendance_rate = round((present_week / total_week * 100), 2) if total_week else 0
        return Response({'total_employees': total_employees, 'present_today': present_today, 'on_leave_today': on_leave_today, 'pending_leave_requests': pending_leave_requests, 'attendance_rate_this_week': attendance_rate})
