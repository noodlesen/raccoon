# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0055_auto_20170411_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='top_comfort',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='top_price',
        ),
    ]
