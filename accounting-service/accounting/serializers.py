from rest_framework import serializers
from accounting.models import BalanceSheet


class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = "__all__"
