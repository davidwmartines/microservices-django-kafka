from person.models import Person
from person.serializers import PersonSerializer
from rest_framework import permissions, viewsets


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.order_by("last_name", "first_name").all()
    serializer_class = PersonSerializer
