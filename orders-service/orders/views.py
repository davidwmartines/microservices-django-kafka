from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import permissions, viewsets


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.order_by("-date_placed").all()
    serializer_class = OrderSerializer
