# Generated by Django 3.2 on 2023-03-13 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
