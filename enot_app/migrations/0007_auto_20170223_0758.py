# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-23 07:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0006_destination'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gcountry',
            old_name='direction',
            new_name='gdirection',
        ),
        migrations.RenameField(
            model_name='gplace',
            old_name='country',
            new_name='gcountry',
        ),
    ]