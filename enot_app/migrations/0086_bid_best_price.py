# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-26 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0085_auto_20170524_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='best_price',
            field=models.BooleanField(default=False),
        ),
    ]
