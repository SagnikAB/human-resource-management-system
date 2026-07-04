from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdminOrHR, IsOwnerOrAdmin
from apps.employees.models import EmployeeProfile
from .models import LeaveType, LeaveRequest, LeaveBalance
from .serializers import LeaveTypeSerializer, LeaveRequestSerializer, LeaveBalanceSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    filterset_fields = ('status', 'leave_type', 'employee')
    ordering_fields = ('created_at', 'start_date')

    def get_queryset(self):
        qs = LeaveRequest.objects.select_related('employee', 'leave_type', 'reviewed_by')
        if not self.request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=self.request.user)
        return qs

    def perform_create(self, serializer):
        employee = generics.get_object_or_404(EmployeeProfile, user=self.request.user, is_deleted=False)
        serializer.save(employee=employee)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_admin_or_hr:
            return super().partial_update(request, *args, **kwargs)
        if obj.employee.user != request.user or obj.status != 'pending' or request.data.get('status') != 'cancelled':
            return Response({'detail': 'You can only cancel your own pending leave requests.'}, status=status.HTTP_403_FORBIDDEN)
        obj.status = 'cancelled'; obj.save(update_fields=['status'])
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrHR])
    def approve(self, request, pk=None):
        obj = self.get_object(); obj.status = 'approved'; obj.reviewed_by = request.user; obj.reviewed_at = timezone.now(); obj.admin_comment = request.data.get('comment', obj.admin_comment); obj.save()
        balance, _ = LeaveBalance.objects.get_or_create(employee=obj.employee, leave_type=obj.leave_type, year=obj.start_date.year, defaults={'allocated_days': obj.leave_type.max_days_per_year})
        balance.used_days += obj.total_days; balance.save(update_fields=['used_days'])
        return Response(self.get_serializer(obj).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrHR])
    def reject(self, request, pk=None):
        obj = self.get_object(); obj.status = 'rejected'; obj.reviewed_by = request.user; obj.reviewed_at = timezone.now(); obj.admin_comment = request.data.get('comment', 'Rejected'); obj.save()
        return Response(self.get_serializer(obj).data)

class LeaveBalanceView(APIView):
    def get(self, request):
        qs = LeaveBalance.objects.select_related('leave_type', 'employee')
        if not request.user.is_admin_or_hr:
            qs = qs.filter(employee__user=request.user)
        return Response(LeaveBalanceSerializer(qs, many=True).data)

class LeaveTypeListView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all().order_by('name')
    serializer_class = LeaveTypeSerializer
    def get_permissions(self):
        if self.request.method == 'GET': return [IsOwnerOrAdmin()]
        return [IsAdminOrHR()]
