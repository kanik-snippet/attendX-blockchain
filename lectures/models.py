from django.db import models
from django.utils import timezone
import uuid

class Lecture(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    teacher = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)  # Assuming User model in 'users' app
    title = models.CharField(max_length=255)
    lecture_number = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    qr_code = models.TextField(blank=True, null=True)  # Store QR Code data as a string
    qr_generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - Lecture {self.lecture_number}"
