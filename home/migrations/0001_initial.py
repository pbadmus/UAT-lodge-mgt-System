# Generated by Django 5.0.6 on 2025-03-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("building", models.CharField(max_length=50)),
                ("room_number", models.CharField(max_length=10)),
                (
                    "room_type",
                    models.CharField(
                        choices=[("single", "Single"), ("shared", "Shared")],
                        max_length=10,
                    ),
                ),
                ("capacity", models.IntegerField()),
                ("occupied", models.IntegerField(default=0)),
            ],
        ),
    ]
