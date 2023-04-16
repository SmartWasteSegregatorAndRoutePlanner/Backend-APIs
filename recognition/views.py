from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from .utils import detect_labels, classify_label, get_unconfigured_labels

# api/recognition/recognize


class ImageLabelRecognizer(APIView):
    '''
    Recognize the labels in image using amazon's Rekognition service
    '''
    permission_classes = [
        IsAuthenticatedOrReadOnly]  # making read only for time being, else esp auth token ould need to be flashed again and again.

    def get(self, request: Request):
        unconfigured_labels = get_unconfigured_labels()

        if unconfigured_labels:
            msg = {
                'unconfigured_labels': unconfigured_labels,
                'msg': 'success',
            }
            status_code = 200
        else:
            msg = {
                'unconfigured_labels': None,
                'msg': 'possibly all labels are configured',
            }
            status_code = 422

        return Response(msg, status=status_code, content_type='application/json')

    def post(self, request: Request):
        msg = {'msg': 'image_file not provided'}
        status_code = 400
        img_file = request.FILES.get('image_file', False)

        # if img_file and not img_file.readable():
        #     msg = {'msg':'image_file not readable'}
        #     status_code = 400
        # elif img_file:
        #     labels = detect_labels(img_file.read())
        #     if labels:
        #         msg = classify_label(labels)
        #         status_code = 200
        #     else:
        #         msg = {
        #             'msg':'service not responding properly',
        #             'error':True,
        #         }

        # below var is only for development purpose
        labels = [
            {
                "Name": "Tin",
                "Confidence": 94.43530731201172,
                "Aliases": []
            },
            {
                "Name": "Plastic",
                "Confidence": 98.45320892333984,
                "Aliases": []
            },
            {
                "Name": "Can",
                "Confidence": 94.63530731201172,
                "Aliases": []
            },
        ]

        msg = classify_label(labels)

        return Response(msg, status=status_code, content_type='application/json')
