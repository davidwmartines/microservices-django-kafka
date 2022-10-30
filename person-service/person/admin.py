from django.contrib import admin
from person import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
