from unittest.util import _MAX_LENGTH
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True)
    aggregatetype = models.CharField(max_length=255, null=False)
    aggregateid = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(null=False)
    type = models.CharField(max_length=255, null=False)
    payload = models.BinaryField()
