# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-04 13:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0009_auto_20170304_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tprequest',
            name='requested_at',
            field=models.DateTimeField(default=datetime.datetime(1979, 6, 30, 7, 0, tzinfo=utc)),
        ),
    ]