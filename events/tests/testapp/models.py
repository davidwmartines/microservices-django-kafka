from django.db import models
from events.decorators import save_event, Config

from uuid import uuid4


@save_event(
    Config(
        type="widget_event",
        to_dict=lambda widget: {"ID": str(widget.id), "Name": widget.name},
    )
)
class Widget(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)

    class Meta:
        app_label = "testapp"
