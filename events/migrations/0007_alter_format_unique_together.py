# Generated by Django 5.0.4 on 2024-10-20 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_format_distance'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='format',
            unique_together={('distance', 'format')},
        ),
    ]