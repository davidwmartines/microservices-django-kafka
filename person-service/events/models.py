from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True)
    aggregatetype = models.CharField(max_length=255, null=False)
    aggregateid = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(null=False)
    event_type = models.CharField(max_length=255, null=False)
    source = models.CharField(max_length=255, null=False, default="")
    content_type = models.CharField(
        max_length=255, null=False, default="application/avro"
    )
    payload = models.BinaryField()
