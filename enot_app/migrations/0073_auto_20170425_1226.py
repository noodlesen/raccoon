# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 12:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0072_dayjob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayjob',
            name='day_number',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(0)]),
        ),
    ]
