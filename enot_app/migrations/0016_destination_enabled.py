# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-04 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0015_auto_20170304_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]