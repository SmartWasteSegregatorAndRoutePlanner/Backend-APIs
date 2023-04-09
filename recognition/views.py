from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from .utils import detect_labels

# api/recognition/recognize
class ImageLabelRecognizer(APIView):
    '''
    Recognize the labels in image using amazon's Rekognition service
    '''
    permission_classes = [IsAuthenticatedOrReadOnly]

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
        #         msg = {
        #             'labels':labels,
        #         }
        #         status_code = 200
        #     else:
        #         msg = {
        #             'msg':'service not responding properly',
        #             'error':True,
        #         }


        # below var is only for development purpose
        labels = [
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
            {
                "Name": "Tin",
                "Confidence": 94.63530731201172,
                "Aliases": []
            }
        ]
        msg = {'labels':labels}

        # TODO: write logic to return only classified trash type
        
        return Response(msg, status=status_code, content_type='application/json')
