
import json
import shutil

from django.conf import settings
from django.core.files import images
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import urlpatterns


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from detector.serializers import ParseImageSerializer
# from detector.source_code import Model


class ImageParserView(GenericViewSet):
    serializer_class = ParseImageSerializer

    @action(methods=['POST'], detail=False)
    def parse_image(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exeption=True)

        for image in serializer.validate_data['images']:
            default_storage.save('/'.join(['images', image.name]), image)

            csv_name = default_storage.save(
                serializer.validate_data['csv_file'].name, serializer.validate_data['csv_file'])

            images_path = '/'.join([settings.MEDIA_ROOT], 'images/')
            box_queue = '/'.join([settings.MEDIA_ROOT, csv_name])

            model = Model(imagesPath=images_path, boxQueue=box_queue)
            response_json = model.run()

            response = HttpResponse(json.dumps(
                response_json), content_type='text/plain; charset=UTF-8')
            response['Content-Disposition'] = (
                'attachment; filename=response.json')
            shutil.rmtree(images_path, ignore_errors=True)

            return response
