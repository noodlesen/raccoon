# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-21 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0045_auto_20170321_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='loader_finished',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='status',
            name='loader_started',
            field=models.IntegerField(default=0),
        ),
    ]
