# Generated by Django 4.1.2 on 2024-04-21 08:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0011_order_deadline"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="deadline",
        ),
    ]