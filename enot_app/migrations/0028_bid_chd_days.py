# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-10 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0027_bid_pre_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='chd_days',
            field=models.IntegerField(default=0),
        ),
    ]
