# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-19 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0006_auto_20171019_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='name',
            field=models.CharField(max_length=45, unique=True, verbose_name='Name'),
        ),
    ]