from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'student')

        user = User.objects.create_user(username=username, password=password, role=role)
        return Response({'message': 'User registered successfully'}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'error': 'Invalid credentials'}, status=400)

from django.utils.timezone import now, timedelta
from .models import QRCode, Attendance
from geopy.distance import geodesic

class GenerateQRView(APIView):
    def post(self, request):
        teacher = request.user
        class_id = request.data.get('class_id')
        expires_at = now() + timedelta(minutes=5)

        qr = QRCode.objects.create(teacher=teacher, class_id=class_id, expires_at=expires_at)
        return Response({'qr_code': qr.qr_image.url})

class VerifyQRView(APIView):
    def post(self, request):
        student = request.user
        qr_id = request.data.get('qr_id')
        student_location = request.data.get('location')

        try:
            qr = QRCode.objects.get(id=qr_id)
            if now() > qr.expires_at:
                return Response({'error': 'QR code expired'}, status=400)

            teacher_location = [20.5937, 78.9629]  # College GPS coordinates (Example)
            distance = geodesic(student_location, teacher_location).meters

            if distance > 50:
                return Response({'error': 'Out of allowed range'}, status=403)

            Attendance.objects.create(student=student, status='Present', location=student_location)
            return Response({'message': 'Attendance marked successfully'})
        except QRCode.DoesNotExist:
            return Response({'error': 'Invalid QR Code'}, status=404)
