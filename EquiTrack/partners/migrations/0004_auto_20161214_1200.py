# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-14 10:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0003_auto_20161209_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='governorate',
        ),
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='gwpcalocation',
            name='region',
        ),
    ]
