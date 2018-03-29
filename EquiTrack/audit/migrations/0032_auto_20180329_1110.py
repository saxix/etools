# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-29 11:10
from __future__ import unicode_literals

from django.db import migrations


def update_email_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('post_office', 'EmailTemplate')

    EmailTemplate.objects.filter(name='audit/staff_member/invite').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('audit', '0031_engagement_exchange_rate'),
        ('post_office', '0004_auto_20160607_0901'),
    ]

    operations = [
        migrations.RunPython(update_email_templates, migrations.RunPython.noop)
    ]
