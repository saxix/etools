# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0002_auto_20180326_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='amount_changed',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount Changed'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='commitment_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='commitment_amount_dc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount DC'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='actual_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Actual Cash Transfer'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='actual_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Actual Cash Transfer Local'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='intervention_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Current FR Amount'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='outstanding_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Outstanding DCT'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='outstanding_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Outstanding DCT Local'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='total_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='FR Overall Amount'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='total_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='FR Overall Amount DC'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='overall_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Overall Amount'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='overall_amount_dc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Overall Amount DC'),
        ),
    ]
