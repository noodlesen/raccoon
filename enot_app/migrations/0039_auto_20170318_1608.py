# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-18 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0038_auto_20170318_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='stat_date',
            field=models.DateField(unique=True),
        ),
    ]
