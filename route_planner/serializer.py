from rest_framework import serializers
from .models import GarbageBinLocation

class GarbageBinLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarbageBinLocation
        fields = ['name', 'garbage_weight', 'latitude', 'longitude']
        