# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-07 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0101_remove_card_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='tags',
            field=models.ManyToManyField(to='enot_app.Tag'),
        ),
        migrations.AddField(
            model_name='quote',
            name='tags',
            field=models.ManyToManyField(to='enot_app.Tag'),
        ),
    ]
