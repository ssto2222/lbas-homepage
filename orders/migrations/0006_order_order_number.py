# Generated by Django 3.2 on 2023-03-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20230223_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default='', max_length=50),
        ),
    ]
