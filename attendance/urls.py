from django.urls import path
from .views import MarkAttendanceAPIView, SubmitAttendanceAPIView

urlpatterns = [
    path('mark/', MarkAttendanceAPIView.as_view(), name='mark-attendance'),
    path('submit/', SubmitAttendanceAPIView.as_view(), name='submit-attendance'),
]
