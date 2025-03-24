# Generated by Django 5.0.6 on 2025-03-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0002_alter_room_room_number_alter_room_room_type_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="status",
            field=models.CharField(
                choices=[
                    ("Active", "Active"),
                    ("Pending", "Pending"),
                    ("Inactive", "Inactive"),
                ],
                max_length=10,
            ),
        ),
    ]
