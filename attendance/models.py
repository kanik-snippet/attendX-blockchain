import uuid
from django.db import models

# Create your models here.
class Attendance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    student = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name="attendances")
    lecture = models.ForeignKey('lectures.Lecture', on_delete=models.CASCADE, related_name="attendances")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')], default='absent')

    def __str__(self):
        return f"{self.student} - {self.lecture} - {self.status}"
