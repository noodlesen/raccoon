# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-31 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0048_trip_rt_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='forced',
            field=models.BooleanField(default=False),
        ),
    ]
