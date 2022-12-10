from django.contrib import admin
from orders import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "date_placed")
