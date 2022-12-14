# Generated by Django 4.1.2 on 2022-10-27 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="type",
            new_name="event_type",
        ),
        migrations.AddField(
            model_name="event",
            name="content_type",
            field=models.CharField(default="application/avro", max_length=255),
        ),
        migrations.AddField(
            model_name="event",
            name="source",
            field=models.CharField(default="", max_length=255),
        ),
    ]
