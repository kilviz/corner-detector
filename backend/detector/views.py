
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from detector.source_code.boxdetector import ImageDetector
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Image
from .serializers import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from drf_spectacular.utils import extend_schema, OpenApiParameter

# detector = ImageDetector(image_path)
# response_json = json.dumps(detector.run())


class ImageProcessingView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=ImageSerializer,
        responses={201: ImageSerializer},
        description="Upload an image to process",
    )
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            original_image = image_instance.image.url
            print(original_image)
            original_image = '/'.join(original_image.split('/')[2:])
            # Применение функции обработки изображения
            json_response = ImageDetector(original_image).run()
            # Сохранение обработанного изображения
            return JsonResponse(json_response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
