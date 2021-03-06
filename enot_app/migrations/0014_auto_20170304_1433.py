# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-04 14:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0013_auto_20170304_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='TpAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('requested_at', models.DateTimeField(default=datetime.datetime(1979, 6, 30, 7, 0, tzinfo=utc))),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2979, 6, 30, 7, 0, tzinfo=utc))),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpr_destination', to='enot_app.Destination')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpr_origin', to='enot_app.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protected', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='tpask',
            name='user_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enot_app.UserQuery'),
        ),
    ]
