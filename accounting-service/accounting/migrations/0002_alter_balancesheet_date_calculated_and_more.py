# Generated by Django 4.1.2 on 2022-10-31 16:03

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balancesheet",
            name="date_calculated",
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.AlterField(
            model_name="balancesheet",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="balancesheet",
            name="person_id",
            field=models.UUIDField(),
        ),
    ]