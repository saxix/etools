# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-24 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisionSyncLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handler_name', models.CharField(max_length=50)),
                ('total_records', models.IntegerField(default=0)),
                ('total_processed', models.IntegerField(default=0)),
                ('successful', models.BooleanField(default=False)),
                ('details', models.CharField(blank=True, max_length=2048, null=True)),
                ('exception_message', models.TextField(blank=True, null=True)),
                ('date_processed', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Country')),
            ],
        ),
    ]
