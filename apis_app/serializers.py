from rest_framework import serializers

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()
    temp = serializers.FloatField()
    description = serializers.CharField()
    icon = serializers.CharField()
    error = serializers.CharField()