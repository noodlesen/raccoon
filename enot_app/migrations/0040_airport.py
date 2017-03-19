# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-19 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0039_auto_20170318_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('size', models.IntegerField(null=True)),
                ('rating', models.IntegerField(null=True)),
                ('iata', models.CharField(max_length=3, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('city_code', models.CharField(max_length=3, null=True)),
                ('country_code', models.CharField(max_length=2, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
                ('alt', models.IntegerField(null=True)),
                ('icao', models.CharField(max_length=4, null=True)),
                ('timezone', models.IntegerField(null=True)),
                ('dst', models.CharField(max_length=1, null=True)),
                ('tzdata', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
