# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0078_auto_20170505_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
