# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-08-04 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0010_auto_20170725_1044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riskcategory',
            old_name='type',
            new_name='category_type',
        ),
        migrations.RenameField(
            model_name='engagement',
            old_name='type',
            new_name='engagement_type',
        ),
        migrations.AlterField(
            model_name='engagement',
            name='engagement_type',
            field=models.CharField(choices=[('audit', 'Audit'), ('ma', 'Micro Accessment'), ('sc', 'Spot Check')], max_length=10, verbose_name='Engagement type'),
        ),
    ]
