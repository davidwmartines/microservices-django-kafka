from accounting.models import BalanceSheet
from accounting.serializers import BalanceSheetSerializer
from rest_framework import permissions, viewsets


class BalanceSheetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BalanceSheet.objects.order_by("-date_calculated").all()
    serializer_class = BalanceSheetSerializer
