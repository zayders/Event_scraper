# Generated by Django 5.0.4 on 2024-07-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_city_event_latitude_event_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]