# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0073_auto_20170425_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
