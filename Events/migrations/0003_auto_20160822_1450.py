# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-22 09:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0002_auto_20160822_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceusage',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 22, 14, 49, 59, 899000)),
        ),
    ]
