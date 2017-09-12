# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-09-12 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields

def reverse(apps, schema_editor):
   return

def remove_all_indicators(apps, schema_editor):
   IndicatorBlueprint = apps.get_model('reports', 'IndicatorBlueprint')
   # use the save method to mark invalid fields
   deleted = IndicatorBlueprint.objects.all().delete()
   if deleted[0]:
       print "Deleted Indicators: {}".format(deleted[0])


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_workspacecounter'),
        ('locations', '0004_auto_20170112_2051'),
        ('reports', '0014_auto_20170908_1307'),
    ]

    operations = [
        migrations.RunPython(remove_all_indicators, reverse_code=reverse),
        migrations.CreateModel(
            name='Disaggregation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Disaggregation by')),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DisaggregationValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value', models.CharField(blank=True, max_length=15, null=True)),
                ('active', models.BooleanField(default=False)),
                ('disaggregation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disaggregation_value', to='reports.Disaggregation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='indicatorblueprint',
            options={'ordering': ['-id']},
        ),
        migrations.RenameField(
            model_name='indicatorblueprint',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='appliedindicator',
            name='disaggregation_logic',
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='cluster_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='cluster_indicator_title',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='locations',
            field=models.ManyToManyField(related_name='applied_indicators', to='locations.Location'),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Section'),
        ),
        migrations.AddField(
            model_name='indicatorblueprint',
            name='calculation_formula_across_locations',
            field=models.CharField(choices=[('sum', 'sum'), ('max', 'max'), ('avg', 'avg'), ('percentage', 'percentage'), ('ratio', 'ratio')], default='sum', max_length=10),
        ),
        migrations.AddField(
            model_name='indicatorblueprint',
            name='calculation_formula_across_periods',
            field=models.CharField(choices=[('sum', 'sum'), ('max', 'max'), ('avg', 'avg'), ('percentage', 'percentage'), ('ratio', 'ratio')], default='sum', max_length=10),
        ),
        migrations.AddField(
            model_name='indicatorblueprint',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='indicatorblueprint',
            name='display_type',
            field=models.CharField(choices=[('number', 'number'), ('percentage', 'percentage'), ('ratio', 'ratio')], default='number', max_length=10),
        ),
        migrations.AddField(
            model_name='indicatorblueprint',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='appliedindicator',
            name='baseline',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appliedindicator',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.IndicatorBlueprint'),
        ),
        migrations.AlterField(
            model_name='appliedindicator',
            name='target',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='indicatorblueprint',
            name='unit',
            field=models.CharField(choices=[('number', 'number'), ('percentage', 'percentage')], default='number', max_length=10),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='disaggregation',
            field=models.ManyToManyField(blank=True, related_name='applied_indicators', to='reports.Disaggregation'),
        ),
    ]
