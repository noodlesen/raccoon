# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-19 13:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0059_trip_tmp_eff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='tmp_eff',
            new_name='rt_eff',
        ),
    ]