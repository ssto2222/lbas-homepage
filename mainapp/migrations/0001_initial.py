# Generated by Django 4.1.2 on 2024-04-19 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(default='', max_length=30)),
                ('zipcode', models.CharField(default='', max_length=8)),
                ('prefecture', models.CharField(default='', max_length=6)),
                ('city', models.CharField(default='', max_length=100)),
                ('address1', models.CharField(default='', max_length=200)),
                ('address2', models.CharField(default='', max_length=50, null=True)),
                ('stripe_id', models.CharField(default='', max_length=30, null=True)),
            ],
        ),
    ]
