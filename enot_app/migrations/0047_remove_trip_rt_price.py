# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-26 10:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0046_auto_20170321_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='rt_price',
        ),
    ]
