# Generated by Django 4.1.2 on 2022-10-31 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("planning", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="person",
            name="last_name",
        ),
        migrations.CreateModel(
            name="BalanceSheet",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("date_calculated", models.DateTimeField()),
                ("assets", models.BigIntegerField(default=0)),
                ("liabilities", models.BigIntegerField(default=0)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="planning.person",
                    ),
                ),
            ],
        ),
    ]