# Generated by Django 4.1.2 on 2022-12-10 11:18

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("customer_id", models.UUIDField()),
                ("date_placed", models.DateTimeField(default=datetime.datetime.utcnow)),
                ("item_count", models.BigIntegerField(default=0)),
            ],
        ),
    ]