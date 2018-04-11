# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-02-21 12:33

from django.db import migrations, models

import EquiTrack


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0004_fix_null_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundscommitmentheader',
            name='document_text',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentheader',
            name='exchange_rate',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Exchange Rate'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentheader',
            name='fc_type',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentheader',
            name='responsible_person',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Responsible'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='fc_ref_number',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Number'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='fr_number',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='FR Number'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='fund',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Fund'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='gl_account',
            field=models.CharField(blank=True, default='', max_length=15, verbose_name='GL Account'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='grant_number',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Grant Number'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='line_item_text',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentitem',
            name='wbs',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='WBS'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='document_text',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Document Text'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='fr_type',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='fr_ref_number',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='Item Number'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='fund',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Fund'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='grant_number',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Grant Number'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='line_item_text',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='fundsreservationitem',
            name='wbs',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='WBS'),
        ),
        migrations.AlterField(
            model_name='grant',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='fundscommitmentheader',
            name='currency',
            field=EquiTrack.fields.CurrencyField(blank=True, choices=[('GIP', 'GIP'), ('KPW', 'KPW'), ('XEU', 'XEU'), ('BHD', 'BHD'), ('BIF', 'BIF'), ('BMD', 'BMD'), ('BSD', 'BSD'), ('YER1', 'YER1'), ('AFN', 'AFN'), ('ALL', 'ALL'), ('AMD', 'AMD'), ('AUD', 'AUD'), ('AZN', 'AZN'), ('BAM', 'BAM'), ('BBD', 'BBD'), ('BDT', 'BDT'), ('BZD', 'BZD'), ('CUP1', 'CUP1'), ('BTN', 'BTN'), ('ZWL', 'ZWL'), ('AWG', 'AWG'), ('CUC', 'CUC'), ('VEF01', 'VEF01'), ('BND', 'BND'), ('BRL', 'BRL'), ('ARS', 'ARS'), ('ETB', 'ETB'), ('EUR', 'EUR'), ('FJD', 'FJD'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHS', 'GHS'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('GYD', 'GYD'), ('HNL', 'HNL'), ('CAD', 'CAD'), ('CDF', 'CDF'), ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'), ('CUP', 'CUP'), ('CVE', 'CVE'), ('DJF', 'DJF'), ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EGP', 'EGP'), ('HRK', 'HRK'), ('LVL', 'LVL'), ('LYD', 'LYD'), ('MAD', 'MAD'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('KWD', 'KWD'), ('KYD', 'KYD'), ('LBP', 'LBP'), ('LKR', 'LKR'), ('MDL', 'MDL'), ('KZT', 'KZT'), ('LRD', 'LRD'), ('BOB', 'BOB'), ('HKD', 'HKD'), ('CHF', 'CHF'), ('KES', 'KES'), ('MYR', 'MYR'), ('NGN', 'NGN'), ('KMF', 'KMF'), ('SCR', 'SCR'), ('SEK', 'SEK'), ('TTD', 'TTD'), ('PKR', 'PKR'), ('NIO', 'NIO'), ('RWF', 'RWF'), ('BWP', 'BWP'), ('JMD', 'JMD'), ('TJS', 'TJS'), ('UYU', 'UYU'), ('RON', 'RON'), ('PYG', 'PYG'), ('SYP', 'SYP'), ('LAK', 'LAK'), ('ERN', 'ERN'), ('SLL', 'SLL'), ('PLN', 'PLN'), ('JOD', 'JOD'), ('ILS', 'ILS'), ('AED', 'AED'), ('NPR', 'NPR'), ('NZD', 'NZD'), ('SGD', 'SGD'), ('JPY', 'JPY'), ('PAB', 'PAB'), ('ZMW', 'ZMW'), ('CZK', 'CZK'), ('SOS', 'SOS'), ('LTL', 'LTL'), ('KGS', 'KGS'), ('SHP', 'SHP'), ('BGN', 'BGN'), ('TOP', 'TOP'), ('MVR', 'MVR'), ('VEF02', 'VEF02'), ('TMT', 'TMT'), ('GMD', 'GMD'), ('MZN', 'MZN'), ('RSD', 'RSD'), ('MWK', 'MWK'), ('PGK', 'PGK'), ('MXN', 'MXN'), ('XAF', 'XAF'), ('VND', 'VND'), ('INR', 'INR'), ('NOK', 'NOK'), ('XPF', 'XPF'), ('SSP', 'SSP'), ('IQD', 'IQD'), ('SRD', 'SRD'), ('SAR', 'SAR'), ('XCD', 'XCD'), ('IRR', 'IRR'), ('KPW01', 'KPW01'), ('HTG', 'HTG'), ('IDR', 'IDR'), ('XOF', 'XOF'), ('ISK', 'ISK'), ('ANG', 'ANG'), ('NAD', 'NAD'), ('MMK', 'MMK'), ('STD', 'STD'), ('VUV', 'VUV'), ('LSL', 'LSL'), ('SVC', 'SVC'), ('KHR', 'KHR'), ('SZL', 'SZL'), ('RUB', 'RUB'), ('UAH', 'UAH'), ('UGX', 'UGX'), ('THB', 'THB'), ('AOA', 'AOA'), ('YER', 'YER'), ('USD', 'USD'), ('UZS', 'UZS'), ('OMR', 'OMR'), ('SBD', 'SBD'), ('TZS', 'TZS'), ('SDG', 'SDG'), ('WST', 'WST'), ('QAR', 'QAR'), ('MOP', 'MOP'), ('MRO', 'MRO'), ('VEF', 'VEF'), ('TRY', 'TRY'), ('ZAR', 'ZAR'), ('HUF', 'HUF'), ('MUR', 'MUR'), ('PHP', 'PHP'), ('BYN', 'BYN'), ('KRW', 'KRW'), ('TND', 'TND'), ('MNT', 'MNT'), ('PEN', 'PEN')], default='', max_length=50, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='fundsreservationheader',
            name='currency',
            field=EquiTrack.fields.CurrencyField(blank=True, choices=[('GIP', 'GIP'), ('KPW', 'KPW'), ('XEU', 'XEU'), ('BHD', 'BHD'), ('BIF', 'BIF'), ('BMD', 'BMD'), ('BSD', 'BSD'), ('YER1', 'YER1'), ('AFN', 'AFN'), ('ALL', 'ALL'), ('AMD', 'AMD'), ('AUD', 'AUD'), ('AZN', 'AZN'), ('BAM', 'BAM'), ('BBD', 'BBD'), ('BDT', 'BDT'), ('BZD', 'BZD'), ('CUP1', 'CUP1'), ('BTN', 'BTN'), ('ZWL', 'ZWL'), ('AWG', 'AWG'), ('CUC', 'CUC'), ('VEF01', 'VEF01'), ('BND', 'BND'), ('BRL', 'BRL'), ('ARS', 'ARS'), ('ETB', 'ETB'), ('EUR', 'EUR'), ('FJD', 'FJD'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHS', 'GHS'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('GYD', 'GYD'), ('HNL', 'HNL'), ('CAD', 'CAD'), ('CDF', 'CDF'), ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'), ('CUP', 'CUP'), ('CVE', 'CVE'), ('DJF', 'DJF'), ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EGP', 'EGP'), ('HRK', 'HRK'), ('LVL', 'LVL'), ('LYD', 'LYD'), ('MAD', 'MAD'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('KWD', 'KWD'), ('KYD', 'KYD'), ('LBP', 'LBP'), ('LKR', 'LKR'), ('MDL', 'MDL'), ('KZT', 'KZT'), ('LRD', 'LRD'), ('BOB', 'BOB'), ('HKD', 'HKD'), ('CHF', 'CHF'), ('KES', 'KES'), ('MYR', 'MYR'), ('NGN', 'NGN'), ('KMF', 'KMF'), ('SCR', 'SCR'), ('SEK', 'SEK'), ('TTD', 'TTD'), ('PKR', 'PKR'), ('NIO', 'NIO'), ('RWF', 'RWF'), ('BWP', 'BWP'), ('JMD', 'JMD'), ('TJS', 'TJS'), ('UYU', 'UYU'), ('RON', 'RON'), ('PYG', 'PYG'), ('SYP', 'SYP'), ('LAK', 'LAK'), ('ERN', 'ERN'), ('SLL', 'SLL'), ('PLN', 'PLN'), ('JOD', 'JOD'), ('ILS', 'ILS'), ('AED', 'AED'), ('NPR', 'NPR'), ('NZD', 'NZD'), ('SGD', 'SGD'), ('JPY', 'JPY'), ('PAB', 'PAB'), ('ZMW', 'ZMW'), ('CZK', 'CZK'), ('SOS', 'SOS'), ('LTL', 'LTL'), ('KGS', 'KGS'), ('SHP', 'SHP'), ('BGN', 'BGN'), ('TOP', 'TOP'), ('MVR', 'MVR'), ('VEF02', 'VEF02'), ('TMT', 'TMT'), ('GMD', 'GMD'), ('MZN', 'MZN'), ('RSD', 'RSD'), ('MWK', 'MWK'), ('PGK', 'PGK'), ('MXN', 'MXN'), ('XAF', 'XAF'), ('VND', 'VND'), ('INR', 'INR'), ('NOK', 'NOK'), ('XPF', 'XPF'), ('SSP', 'SSP'), ('IQD', 'IQD'), ('SRD', 'SRD'), ('SAR', 'SAR'), ('XCD', 'XCD'), ('IRR', 'IRR'), ('KPW01', 'KPW01'), ('HTG', 'HTG'), ('IDR', 'IDR'), ('XOF', 'XOF'), ('ISK', 'ISK'), ('ANG', 'ANG'), ('NAD', 'NAD'), ('MMK', 'MMK'), ('STD', 'STD'), ('VUV', 'VUV'), ('LSL', 'LSL'), ('SVC', 'SVC'), ('KHR', 'KHR'), ('SZL', 'SZL'), ('RUB', 'RUB'), ('UAH', 'UAH'), ('UGX', 'UGX'), ('THB', 'THB'), ('AOA', 'AOA'), ('YER', 'YER'), ('USD', 'USD'), ('UZS', 'UZS'), ('OMR', 'OMR'), ('SBD', 'SBD'), ('TZS', 'TZS'), ('SDG', 'SDG'), ('WST', 'WST'), ('QAR', 'QAR'), ('MOP', 'MOP'), ('MRO', 'MRO'), ('VEF', 'VEF'), ('TRY', 'TRY'), ('ZAR', 'ZAR'), ('HUF', 'HUF'), ('MUR', 'MUR'), ('PHP', 'PHP'), ('BYN', 'BYN'), ('KRW', 'KRW'), ('TND', 'TND'), ('MNT', 'MNT'), ('PEN', 'PEN')], default='', max_length=50, verbose_name='Currency'),
        ),
    ]
