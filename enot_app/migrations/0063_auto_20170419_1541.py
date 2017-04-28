# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-19 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0062_trip_days_to'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Airline',
            new_name='Carrier',
        ),
        migrations.AddField(
            model_name='trip',
            name='days_to_text',
            field=models.CharField(max_length=10, null=True),
        ),
    ]