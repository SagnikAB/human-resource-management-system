from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from hrms.views import (
    AttendanceViewSet,
    AuthSignInView,
    AuthSignUpView,
    EmployeeViewSet,
    LeaveRequestViewSet,
    PayrollRecordViewSet,
    SalaryStructureViewSet,
)

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employees")
router.register("attendance", AttendanceViewSet, basename="attendance")
router.register("leave-requests", LeaveRequestViewSet, basename="leave-requests")
router.register("payroll", PayrollRecordViewSet, basename="payroll")
router.register("salary-structures", SalaryStructureViewSet, basename="salary-structures")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/signup/", AuthSignUpView.as_view(), name="auth-signup"),
    path("api/auth/signin/", AuthSignInView.as_view(), name="auth-signin"),
    path("api/", include(router.urls)),
]
