# Generated by Django 5.0.4 on 2024-06-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_format_remove_event_distance_remove_event_format_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='formats',
            field=models.ManyToManyField(to='events.format'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='format',
            name='format',
            field=models.CharField(max_length=100),
        ),
    ]