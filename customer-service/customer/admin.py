from django.contrib import admin
from customer import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
