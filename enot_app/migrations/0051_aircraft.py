# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0050_auto_20170331_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('count', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
    ]
