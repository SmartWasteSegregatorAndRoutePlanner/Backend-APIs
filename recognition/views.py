from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from base64 import b64encode

from .utils import detect_labels

# api/recognition/recognize


class ImageLabelRecognizer(APIView):
    '''
    Recognize the labels in image using amazon's Rekognition service
    '''

    def post(self, request: Request):
        msg = {'msg': 'image_file not provided'}
        status_code = 400
        file_obj = request.FILES.get('image_file', False)

        # if file_obj and not file_obj.readable():
        #     msg = {'msg':'image_file not readable'}
        #     status_code = 400
        # elif file_obj:
        #     labels = detect_labels(file_obj.read())
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
