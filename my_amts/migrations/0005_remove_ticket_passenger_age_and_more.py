# Generated by Django 5.1.4 on 2025-02-12 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_amts', '0004_alter_searchhistory_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='passenger_age',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='passenger_name',
        ),
    ]
