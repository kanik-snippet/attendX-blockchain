from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)  # Role-based authentication
    is_student = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
