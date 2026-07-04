from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, EmployeeAttendanceView
router = DefaultRouter()
router.register('', AttendanceViewSet, basename='attendance')
urlpatterns = router.urls + [path('employee/<int:employee_id>/', EmployeeAttendanceView.as_view(), name='employee-attendance')]
