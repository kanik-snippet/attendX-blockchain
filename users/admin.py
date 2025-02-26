from django.contrib import admin
from .models import Teacher, Student, CustomUser  # Import your models

# Registering models to the Django admin site
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(CustomUser)
