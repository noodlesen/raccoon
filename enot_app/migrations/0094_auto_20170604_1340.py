# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-04 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enot_app', '0093_auto_20170604_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('link', models.CharField(max_length=255)),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='enot_app.GPlace')),
                ('tags', models.ManyToManyField(to='enot_app.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='enot_app.GPlace'),
        ),
    ]