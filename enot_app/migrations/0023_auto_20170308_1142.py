# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-08 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0022_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='rating',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
