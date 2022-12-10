from rest_framework import serializers


class AwardSerializer(serializers.Serializer):
    points = serializers.FloatField()
