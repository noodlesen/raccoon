# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0077_issue_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayjob',
            name='algorithm',
            field=models.CharField(choices=[('TP', 'Aviasales only'), ('OTHER', 'Other')], default='TP', max_length=10),
        ),
        migrations.AddField(
            model_name='trip',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
