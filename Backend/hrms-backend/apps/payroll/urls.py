from django.urls import path
from .views import SalaryStructureListView, SalaryStructureDetailView, PayrollRecordListView, PayrollRecordDetailView, GeneratePayrollView
urlpatterns = [
    path('salary-structure/', SalaryStructureListView.as_view(), name='salary-structure-list'),
    path('salary-structure/<int:employee_id>/', SalaryStructureDetailView.as_view(), name='salary-structure-detail'),
    path('records/', PayrollRecordListView.as_view(), name='payroll-record-list'),
    path('records/<int:pk>/', PayrollRecordDetailView.as_view(), name='payroll-record-detail'),
    path('generate/', GeneratePayrollView.as_view(), name='generate-payroll'),
]
