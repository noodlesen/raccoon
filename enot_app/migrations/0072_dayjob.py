# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0071_auto_20170425_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.IntegerField(unique=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enot_app.City')),
            ],
        ),
    ]