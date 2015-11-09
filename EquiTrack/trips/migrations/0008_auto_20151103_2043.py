# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_trip_status_fsm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=django_fsm.FSMField(default='planned', max_length=32L, choices=[('planned', 'Planned'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]),
            preserve_default=True,
        ),
    ]
