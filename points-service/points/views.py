from django.shortcuts import get_object_or_404
from points.calculators import PointsCalculator
from points.models import Customer
from points.serializers import AwardSerializer
from rest_framework import permissions, views
from rest_framework.response import Response


class AwardView(views.APIView):
    def get(self, request, customer_id, format=None):
        customer = get_object_or_404(Customer, id=customer_id)
        calculator = PointsCalculator(customer)
        serializer = AwardSerializer(calculator.award())
        return Response(serializer.data)
