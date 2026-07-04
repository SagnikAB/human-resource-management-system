from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet, LeaveBalanceView, LeaveTypeListView
router = DefaultRouter()
router.register('requests', LeaveRequestViewSet, basename='leave-requests')
urlpatterns = router.urls + [path('balance/', LeaveBalanceView.as_view(), name='leave-balance'), path('types/', LeaveTypeListView.as_view(), name='leave-types')]
