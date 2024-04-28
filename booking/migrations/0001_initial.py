# Generated by Django 4.1.2 on 2024-04-28 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="名前"
                    ),
                ),
                ("email", models.EmailField(max_length=100, verbose_name="E-mail")),
                (
                    "line_id",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="LINE ID"
                    ),
                ),
                (
                    "remarks",
                    models.TextField(blank=True, default="", verbose_name="備考"),
                ),
                (
                    "start",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="開始時間"
                    ),
                ),
                (
                    "end",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="終了時間"
                    ),
                ),
            ],
        ),
    ]
