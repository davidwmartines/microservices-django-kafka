from django.contrib import admin
from accounting import models


@admin.register(models.BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ("id", "person_id", "date_calculated")
