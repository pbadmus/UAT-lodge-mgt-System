# Generated by Django 5.0.6 on 2025-03-13 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="room_number",
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name="room",
            name="room_type",
            field=models.CharField(
                choices=[("Single", "Single"), ("Shared", "Shared")], max_length=10
            ),
        ),
        migrations.CreateModel(
            name="Staff",
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
                ("name", models.CharField(max_length=70)),
                (
                    "room_type",
                    models.CharField(
                        choices=[("Single", "Single"), ("Shared", "Shared")],
                        max_length=10,
                    ),
                ),
                ("date_entry", models.DateField(auto_now_add=True)),
                ("date_exit", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Pending", "Pending"),
                            ("Not Active", "Not Active"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "room_number",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="home.room",
                    ),
                ),
            ],
        ),
    ]
