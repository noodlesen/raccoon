# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-10 06:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0024_subscriber_tester'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='destination',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bid_destination', to='enot_app.Destination'),
        ),
        migrations.AddField(
            model_name='bid',
            name='origin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bid_origin', to='enot_app.Destination'),
        ),
    ]