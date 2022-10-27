from django.db import models


class Person(models.Model):
    """
    Represents a human known to the Planning Service.
    Person data comes from the microservice ecosystem
    via the person entity state stream.  The person data
    in this service is not considered authortative and
    is not managed here.
    """

    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name if self.last_name else '?'}, {self.first_name if self.first_name else '?'} | {self.id}"
