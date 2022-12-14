# Generated by Django 4.1.2 on 2022-12-10 11:15

import datetime
from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("first_name", models.CharField(default="", max_length=50)),
                ("last_name", models.CharField(default="", max_length=50)),
                (
                    "date_established",
                    models.DateTimeField(
                        blank=True, default=datetime.datetime.now, null=True
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
