from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.timezone import now
from .models import Attendance
from .serializers import AttendanceSerializer
from lectures.models import Lecture

class MarkAttendanceAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Mark Attendance",
        operation_description="Students scan the QR code to mark their attendance.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'lecture_id': openapi.Schema(type=openapi.TYPE_STRING, description="Lecture ID"),
            }
        ),
        responses={201: AttendanceSerializer()},
    )
    def post(self, request, *args, **kwargs):
        student = request.user
        lecture_id = request.data.get('lecture_id')

        try:
            lecture = Lecture.objects.get(id=lecture_id)
        except Lecture.DoesNotExist:
            return Response({"error": "Invalid lecture ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already marked
        if Attendance.objects.filter(student=student, lecture=lecture).exists():
            return Response({"error": "Attendance already marked"}, status=status.HTTP_400_BAD_REQUEST)

        # Mark attendance
        attendance = Attendance.objects.create(student=student, lecture=lecture, status="present")
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)


class SubmitAttendanceAPIView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Submit Attendance",
        operation_description="Teacher submits final attendance, marking students absent if they did not scan the QR code.",
        responses={200: "Attendance submitted"},
    )
    def put(self, request, *args, **kwargs):
        teacher = request.user

        # Get lectures by this teacher
        lectures = Lecture.objects.filter(teacher=teacher)
        if not lectures.exists():
            return Response({"error": "No lectures found for this teacher"}, status=status.HTTP_400_BAD_REQUEST)

        for lecture in lectures:
            students_present = Attendance.objects.filter(lecture=lecture).values_list('student', flat=True)

            # Mark absent students
            students_absent = request.user.__class__.objects.exclude(id__in=students_present)
            for student in students_absent:
                Attendance.objects.get_or_create(student=student, lecture=lecture, defaults={"status": "absent"})

        return Response({"message": "Attendance submitted"}, status=status.HTTP_200_OK)
