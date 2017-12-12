# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-11-27 22:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workplan', '0002_milestone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='tagged_users',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='workplan',
        ),
        migrations.RemoveField(
            model_name='coverpage',
            name='workplan_project',
        ),
        migrations.RemoveField(
            model_name='coverpagebudget',
            name='cover_page',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='result_wp_property',
        ),
        migrations.RemoveField(
            model_name='quarter',
            name='workplan',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='geotag',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='partners',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='responsible_persons',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='result',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='sections',
        ),
        migrations.RemoveField(
            model_name='resultworkplanproperty',
            name='workplan',
        ),
        migrations.RemoveField(
            model_name='workplan',
            name='country_programme',
        ),
        migrations.RemoveField(
            model_name='workplanproject',
            name='workplan',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CoverPage',
        ),
        migrations.DeleteModel(
            name='CoverPageBudget',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.DeleteModel(
            name='Milestone',
        ),
        migrations.DeleteModel(
            name='Quarter',
        ),
        migrations.DeleteModel(
            name='ResultWorkplanProperty',
        ),
        migrations.DeleteModel(
            name='Workplan',
        ),
        migrations.DeleteModel(
            name='WorkplanProject',
        ),
    ]
