# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0026_auto_20161013_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultstructure',
            options={'ordering': ['name'], 'verbose_name': 'Humanitarian Response Plan', 'verbose_name_plural': 'Humanitarian Response Plans'},
        ),
        migrations.AlterField(
            model_name='goal',
            name='result_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Humanitarian Response Plan', blank=True, to='reports.ResultStructure', null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='result_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Humanitarian Response Plan', blank=True, to='reports.ResultStructure', null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_structure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name=b'Humanitarian Response Plan', blank=True, to='reports.ResultStructure', null=True),
        ),
    ]
