from rest_framework import serializers


class CalculatedRatioSerializer(serializers.Serializer):
    ratio = serializers.FloatField()
    benchmark = serializers.FloatField()
    status = serializers.CharField()


class FinancialRatioSerializer(serializers.Serializer):
    name = serializers.CharField()
    result = CalculatedRatioSerializer()
