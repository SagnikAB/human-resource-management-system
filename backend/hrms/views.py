from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AttendanceRecord, AuditLog, Employee, LeaveRequest, PayrollRecord, SalaryStructure
from .permissions import IsHrUser, is_hr_user
from .serializers import (
    AttendanceRecordSerializer,
    EmployeeSelfUpdateSerializer,
    EmployeeSerializer,
    LeaveDecisionSerializer,
    LeaveRequestSerializer,
    PayrollRecordSerializer,
    SalaryStructureSerializer,
    SignInSerializer,
    SignUpSerializer,
)

User = get_user_model()


def auth_payload(user):
    token, _ = Token.objects.get_or_create(user=user)
    employee = getattr(user, "employee_profile", None)
    return {
        "token": token.key,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": employee.role if employee else None,
            "employee_id": employee.id if employee else None,
        },
    }


class AuthSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(auth_payload(user), status=status.HTTP_201_CREATED)


class AuthSignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(auth_payload(serializer.validated_data["user"]))


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Employee.objects.select_related("user", "manager").order_by("department", "last_name")
        if is_hr_user(self.request.user):
            return queryset
        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in {"list", "create", "update", "partial_update", "destroy"}:
            return [IsHrUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        employee = request.user.employee_profile
        if request.method == "PATCH":
            serializer = EmployeeSelfUpdateSerializer(employee, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(EmployeeSerializer(employee).data)
        return Response(EmployeeSerializer(employee).data)

    def perform_update(self, serializer):
        employee = serializer.save()
        AuditLog.objects.create(
            actor=self.request.user,
            action="EMPLOYEE_UPDATED",
            entity="Employee",
            entity_id=str(employee.id),
            metadata=serializer.validated_data,
        )


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AttendanceRecord.objects.select_related("employee")
        employee_id = self.request.query_params.get("employee")
        if is_hr_user(self.request.user):
            return queryset.filter(employee_id=employee_id) if employee_id else queryset
        return queryset.filter(employee=self.request.user.employee_profile)

    @action(detail=False, methods=["post"], url_path="check-in")
    def check_in(self, request):
        employee = request.user.employee_profile
        record, _ = AttendanceRecord.objects.update_or_create(
            employee=employee,
            work_date=timezone.localdate(),
            defaults={
                "check_in_at": timezone.now(),
                "status": AttendanceRecord.Status.PRESENT,
                "notes": request.data.get("notes", ""),
            },
        )
        return Response(AttendanceRecordSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="check-out")
    def check_out(self, request):
        employee = request.user.employee_profile
        record = AttendanceRecord.objects.get(employee=employee, work_date=timezone.localdate())
        record.check_out_at = timezone.now()
        record.save(update_fields=["check_out_at", "updated_at"])
        return Response(AttendanceRecordSerializer(record).data)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = LeaveRequest.objects.select_related("employee", "reviewer")
        status_filter = self.request.query_params.get("status")
        employee_id = self.request.query_params.get("employee")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if is_hr_user(self.request.user):
            return queryset.filter(employee_id=employee_id) if employee_id else queryset
        return queryset.filter(employee=self.request.user.employee_profile)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee_profile)

    @action(detail=True, methods=["patch"], permission_classes=[IsHrUser])
    def decision(self, request, pk=None):
        leave_request = self.get_object()
        serializer = LeaveDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        leave_request.status = serializer.validated_data["status"]
        leave_request.reviewer = request.user
        leave_request.reviewer_note = serializer.validated_data.get("reviewer_note", "")
        leave_request.reviewed_at = timezone.now()
        leave_request.save()
        AuditLog.objects.create(
            actor=request.user,
            action=f"LEAVE_{leave_request.status}",
            entity="LeaveRequest",
            entity_id=str(leave_request.id),
            metadata={"employee_id": leave_request.employee_id},
        )
        return Response(LeaveRequestSerializer(leave_request).data)


class SalaryStructureViewSet(viewsets.ModelViewSet):
    serializer_class = SalaryStructureSerializer
    permission_classes = [IsHrUser]

    def get_queryset(self):
        return SalaryStructure.objects.select_related("employee").order_by("-effective_from")

    def perform_create(self, serializer):
        employee = serializer.validated_data["employee"]
        SalaryStructure.objects.filter(employee=employee, is_active=True).update(is_active=False)
        structure = serializer.save(is_active=True)
        AuditLog.objects.create(
            actor=self.request.user,
            action="SALARY_STRUCTURE_UPDATED",
            entity="SalaryStructure",
            entity_id=str(structure.id),
            metadata={"employee_id": employee.id},
        )


class PayrollRecordViewSet(viewsets.ModelViewSet):
    serializer_class = PayrollRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PayrollRecord.objects.select_related("employee")
        if is_hr_user(self.request.user):
            employee_id = self.request.query_params.get("employee")
            return queryset.filter(employee_id=employee_id) if employee_id else queryset
        return queryset.filter(employee=self.request.user.employee_profile, published_at__isnull=False)

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsHrUser()]
        return [IsAuthenticated()]
