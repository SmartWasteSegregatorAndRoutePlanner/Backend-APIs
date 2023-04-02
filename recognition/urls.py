from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ImageLabelRecognizer


urlpatterns = [
    path('recognize', ImageLabelRecognizer.as_view(), name='image-label-recognizer'),
]
