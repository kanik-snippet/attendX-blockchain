from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import qrcode
import base64
from io import BytesIO
from django.utils.timezone import now
from .models import Lecture
from .serializers import LectureSerializer

class GenerateQRCodeAPIView(generics.UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Generate a QR Code for a Lecture",
        operation_description="Generates a QR code for a specific lecture and stores it in the database.",
        responses={200: LectureSerializer()},
    )
    def put(self, request, *args, **kwargs):
        lecture = self.get_object()

        # Generate QR code
        qr = qrcode.make(f"lecture_id:{lecture.id}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_data = base64.b64encode(buffer.getvalue()).decode()

        # Save QR code data
        lecture.qr_code = qr_data
        lecture.qr_generated_at = now()
        lecture.save()

        return Response(LectureSerializer(lecture).data, status=status.HTTP_200_OK)
