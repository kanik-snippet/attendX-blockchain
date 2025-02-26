from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from .models import Attendance
from users.models import Teacher, Student

@receiver(post_save, sender=Attendance)
def update_attendance_stats(sender, instance, created, **kwargs):
    if created:
        # Update Teacher Stats
        teacher = instance.lecture.teacher
        teacher.total_lectures_given += 1
        teacher.total_students_present += instance.present_students.count()
        teacher.total_students_absent += instance.absent_students.count()
        teacher.save()

        # Update Student Stats
        for student in instance.present_students.all():
            student.lectures_attended_today += 1
            student.lectures_attended_week += 1
            student.lectures_attended_month += 1
            student.lectures_attended_semester += 1
            student.save()
