# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-22 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0105_card_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='direct',
            field=models.BooleanField(default=False),
        ),
    ]