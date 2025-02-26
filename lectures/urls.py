from django.urls import path
from .views import GenerateQRCodeAPIView

urlpatterns = [
    path('generate-qr/<uuid:pk>/', GenerateQRCodeAPIView.as_view(), name='generate-qr'),
]
