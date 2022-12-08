from planning.models import Person
from planning.serializers import FinancialRatioSerializer
from planning.ratios import NetWorthToTotalAssets
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


class FinancialRatiosView(views.APIView):
    def get(self, request, person_id, format=None):
        person = get_object_or_404(Person, id=person_id)
        calculator = NetWorthToTotalAssets(person)
        serializer = FinancialRatioSerializer([calculator], many=True)
        return Response(serializer.data)
