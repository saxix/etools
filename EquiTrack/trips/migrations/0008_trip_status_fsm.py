# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_auto_20151027_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='status_fsm',
            field=django_fsm.FSMField(default='planned', max_length=50, choices=[('planned', 'Planned'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]),
            preserve_default=True,
        ),
    ]
