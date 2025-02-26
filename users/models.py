import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta

class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    subjects = models.TextField(help_text="Comma-separated subjects")
    
    # New fields
    total_lectures_given = models.PositiveIntegerField(default=0)
    total_students_present = models.PositiveIntegerField(default=0)
    total_students_absent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Teacher: {self.user.username} ({self.department})"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    year = models.IntegerField()
    semester = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # New fields
    lectures_attended_today = models.PositiveIntegerField(default=0)
    lectures_attended_week = models.PositiveIntegerField(default=0)
    lectures_attended_month = models.PositiveIntegerField(default=0)
    lectures_attended_semester = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Student: {self.user.username} ({self.branch}, Year {self.year})"
