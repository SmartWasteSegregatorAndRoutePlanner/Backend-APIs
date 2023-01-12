from rest_framework import serializers 

class MapCordinateSerializer(serializers.Serializer):
    long = serializers.FloatField()
    lat = serializers.FloatField()
    name = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance