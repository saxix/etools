# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-26 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0015_auto_20171020_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedindicator',
            name='lower_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_indicators', to='reports.LowerResult', verbose_name='PD Result'),
        ),
        migrations.AlterField(
            model_name='lowerresult',
            name='result_link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ll_results', to='partners.InterventionResultLink'),
        ),
    ]