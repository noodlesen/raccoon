# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-07 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0098_auto_20170607_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='sex',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
