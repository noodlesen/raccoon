# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-07 20:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0100_remove_quote_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='tags',
        ),
    ]
