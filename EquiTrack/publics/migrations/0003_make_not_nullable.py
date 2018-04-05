# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-02-19 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publics', '0002_fix_null_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='dsa_code',
            field=models.CharField(default='', max_length=3, verbose_name='DSA Code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='iso_2',
            field=models.CharField(default='', max_length=2, verbose_name='ISO code 2'),
        ),
        migrations.AlterField(
            model_name='country',
            name='iso_3',
            field=models.CharField(default='', max_length=3, verbose_name='ISO code 3'),
        ),
        migrations.AlterField(
            model_name='dsarateupload',
            name='status',
            field=models.CharField(blank=True, choices=[('uploaded', 'Uploaded'), ('processing', 'Processing'), ('failed', 'Failed'), ('done', 'Done')], default='', max_length=64, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='travelagent',
            name='city',
            field=models.CharField(default='', max_length=128, verbose_name='City'),
        ),
    ]