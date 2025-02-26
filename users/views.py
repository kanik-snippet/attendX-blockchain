from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key, 'user_id': request.user.id, 'is_teacher': request.user.is_teacher})

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))
