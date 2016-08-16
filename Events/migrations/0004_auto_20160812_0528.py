# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-11 23:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0003_auto_20160810_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventslist',
            name='year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='resourceusage',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 12, 5, 28, 46, 660000)),
        ),
    ]