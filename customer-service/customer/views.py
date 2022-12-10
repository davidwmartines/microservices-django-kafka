from customer.models import Customer
from customer.serializers import CustomerSerializer
from rest_framework import permissions, viewsets


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.order_by("last_name", "first_name").all()
    serializer_class = CustomerSerializer
