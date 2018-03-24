# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-24 13:36
from __future__ import unicode_literals

import EquiTrack.fields
import EquiTrack.mixins
import EquiTrack.utils
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import django_fsm
import model_utils.fields
import partners.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('agreement_type', models.CharField(choices=[('PCA', 'Programme Cooperation Agreement'), ('SSFA', 'Small Scale Funding Agreement'), ('MOU', 'Memorandum of Understanding')], max_length=10, verbose_name='Agreement Type')),
                ('agreement_number', models.CharField(blank=True, max_length=45, unique=True, verbose_name='Reference Number')),
                ('attached_agreement', models.FileField(blank=True, max_length=1024, upload_to=partners.models.get_agreement_path, verbose_name='Attached Agreement')),
                ('start', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('signed_by_unicef_date', models.DateField(blank=True, null=True, verbose_name='Signed By UNICEF Date')),
                ('signed_by_partner_date', models.DateField(blank=True, null=True, verbose_name='Signed By Partner Date')),
                ('status', django_fsm.FSMField(blank=True, choices=[('draft', 'Draft'), ('signed', 'Signed'), ('ended', 'Ended'), ('suspended', 'Suspended'), ('terminated', 'Terminated')], default='draft', max_length=32, verbose_name='Status')),
            ],
            options={
                'ordering': ['-created'],
            },
            managers=[
                ('view_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AgreementAmendment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=5, verbose_name='Number')),
                ('signed_amendment', models.FileField(blank=True, max_length=1024, null=True, upload_to=partners.models.get_agreement_amd_file_path, verbose_name='Signed Amendment')),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Change IP name', 'Change in Legal Name of Implementing Partner'), ('Change authorized officer', 'Change Authorized Officer(s)'), ('Change banking info', 'Banking Information'), ('Change in clause', 'Change in clause')], max_length=50), size=None)),
                ('signed_date', models.DateField(blank=True, null=True, verbose_name='Signed Date')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('view_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.CharField(choices=[('Micro Assessment', 'Micro Assessment'), ('Simplified Checklist', 'Simplified Checklist'), ('Scheduled Audit report', 'Scheduled Audit report'), ('Special Audit report', 'Special Audit report'), ('Other', 'Other')], max_length=50, verbose_name='Type')),
                ('names_of_other_agencies', models.CharField(blank=True, help_text='List the names of the other agencies they have worked with', max_length=255, null=True, verbose_name='Other Agencies')),
                ('expected_budget', models.IntegerField(blank=True, null=True, verbose_name='Planned amount')),
                ('notes', models.CharField(blank=True, help_text='Note any special requests to be considered during the assessment', max_length=255, null=True, verbose_name='Special requests')),
                ('requested_date', models.DateField(auto_now_add=True, verbose_name='Requested Date')),
                ('planned_date', models.DateField(blank=True, null=True, verbose_name='Planned Date')),
                ('completed_date', models.DateField(blank=True, null=True, verbose_name='Completed Date')),
                ('rating', models.CharField(choices=[('high', 'High'), ('significant', 'Significant'), ('medium', 'Medium'), ('low', 'Low')], default='high', max_length=50, verbose_name='Rating')),
                ('report', models.FileField(blank=True, max_length=1024, null=True, upload_to=partners.models.get_assesment_path, verbose_name='Report')),
                ('current', models.BooleanField(default=False, verbose_name='Basis for risk rating')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DirectCashTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fc_ref', models.CharField(max_length=50)),
                ('amount_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('liquidation_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('outstanding_balance_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_less_than_3_Months_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_3_to_6_months_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_6_to_9_months_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_more_than_9_Months_usd', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FACE', 'FACE'), ('Progress Report', 'Progress Report'), ('Partnership Review', 'Partnership Review'), ('Final Partnership Review', 'Final Partnership Review'), ('Correspondence', 'Correspondence'), ('Supply/Distribution Plan', 'Supply/Distribution Plan'), ('Other', 'Other')], max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundingCommitment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end')),
                ('fr_number', models.CharField(max_length=50)),
                ('wbs', models.CharField(max_length=50)),
                ('fc_type', models.CharField(max_length=50)),
                ('fc_ref', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('fr_item_amount_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('agreement_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('commitment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('expenditure_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('document_type', models.CharField(choices=[('PD', 'Programme Document'), ('SHPD', 'Simplified Humanitarian Programme Document'), ('SSFA', 'SSFA')], max_length=255, verbose_name='Document Type')),
                ('number', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='Reference Number')),
                ('title', models.CharField(max_length=256, verbose_name='Document Title')),
                ('status', django_fsm.FSMField(blank=True, choices=[('draft', 'Draft'), ('signed', 'Signed'), ('active', 'Active'), ('ended', 'Ended'), ('closed', 'Closed'), ('suspended', 'Suspended'), ('terminated', 'Terminated')], default='draft', max_length=32, verbose_name='Status')),
                ('start', models.DateField(blank=True, help_text='The date the Intervention will start', null=True, verbose_name='Start Date')),
                ('end', models.DateField(blank=True, help_text='The date the Intervention will end', null=True, verbose_name='End Date')),
                ('submission_date', models.DateField(blank=True, help_text='The date the partner submitted complete PD/SSFA documents to Unicef', null=True, verbose_name='Document Submission Date by CSO')),
                ('submission_date_prc', models.DateField(blank=True, help_text='The date the documents were submitted to the PRC', null=True, verbose_name='Submission Date to PRC')),
                ('review_date_prc', models.DateField(blank=True, help_text='The date the PRC reviewed the partnership', null=True, verbose_name='Review Date by PRC')),
                ('prc_review_document', models.FileField(blank=True, max_length=1024, null=True, upload_to=partners.models.get_prc_intervention_file_path, verbose_name='Review Document by PRC')),
                ('signed_pd_document', models.FileField(blank=True, max_length=1024, null=True, upload_to=partners.models.get_prc_intervention_file_path, verbose_name='Signed PD Document')),
                ('signed_by_unicef_date', models.DateField(blank=True, null=True, verbose_name='Signed by UNICEF Date')),
                ('signed_by_partner_date', models.DateField(blank=True, null=True, verbose_name='Signed by Partner Date')),
                ('contingency_pd', models.BooleanField(default=False, verbose_name='Contingency PD')),
                ('population_focus', models.CharField(blank=True, max_length=130, null=True, verbose_name='Population Focus')),
                ('in_amendment', models.BooleanField(default=False, verbose_name='Amendment Open')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='Metadata')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='InterventionAmendment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('dates', 'Dates'), ('results', 'Results'), ('budget', 'Budget'), ('other', 'Other')], max_length=50), size=None)),
                ('other_description', models.CharField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('signed_date', models.DateField(null=True, verbose_name='Signed Date')),
                ('amendment_number', models.IntegerField(default=0, verbose_name='Number')),
                ('signed_amendment', models.FileField(max_length=1024, upload_to=partners.models.get_intervention_amendment_file_path, verbose_name='Amendment Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterventionAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('attachment', models.FileField(max_length=1024, upload_to=partners.models.get_intervention_attachments_file_path)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='InterventionBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('partner_contribution', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('unicef_cash', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('in_kind_amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='UNICEF Supplies')),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('partner_contribution_local', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('unicef_cash_local', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('in_kind_amount_local', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='UNICEF Supplies Local')),
                ('currency', EquiTrack.fields.CurrencyField(blank=True, choices=[('GIP', 'GIP'), ('KPW', 'KPW'), ('XEU', 'XEU'), ('BHD', 'BHD'), ('BIF', 'BIF'), ('BMD', 'BMD'), ('BSD', 'BSD'), ('YER1', 'YER1'), ('AFN', 'AFN'), ('ALL', 'ALL'), ('AMD', 'AMD'), ('AUD', 'AUD'), ('AZN', 'AZN'), ('BAM', 'BAM'), ('BBD', 'BBD'), ('BDT', 'BDT'), ('BZD', 'BZD'), ('CUP1', 'CUP1'), ('BTN', 'BTN'), ('ZWL', 'ZWL'), ('AWG', 'AWG'), ('CUC', 'CUC'), ('VEF01', 'VEF01'), ('BND', 'BND'), ('BRL', 'BRL'), ('ARS', 'ARS'), ('ETB', 'ETB'), ('EUR', 'EUR'), ('FJD', 'FJD'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHS', 'GHS'), ('GNF', 'GNF'), ('GTQ', 'GTQ'), ('GYD', 'GYD'), ('HNL', 'HNL'), ('CAD', 'CAD'), ('CDF', 'CDF'), ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'), ('CUP', 'CUP'), ('CVE', 'CVE'), ('DJF', 'DJF'), ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EGP', 'EGP'), ('HRK', 'HRK'), ('LVL', 'LVL'), ('LYD', 'LYD'), ('MAD', 'MAD'), ('MGA', 'MGA'), ('MKD', 'MKD'), ('KWD', 'KWD'), ('KYD', 'KYD'), ('LBP', 'LBP'), ('LKR', 'LKR'), ('MDL', 'MDL'), ('KZT', 'KZT'), ('LRD', 'LRD'), ('BOB', 'BOB'), ('HKD', 'HKD'), ('CHF', 'CHF'), ('KES', 'KES'), ('MYR', 'MYR'), ('NGN', 'NGN'), ('KMF', 'KMF'), ('SCR', 'SCR'), ('SEK', 'SEK'), ('TTD', 'TTD'), ('PKR', 'PKR'), ('NIO', 'NIO'), ('RWF', 'RWF'), ('BWP', 'BWP'), ('JMD', 'JMD'), ('TJS', 'TJS'), ('UYU', 'UYU'), ('RON', 'RON'), ('PYG', 'PYG'), ('SYP', 'SYP'), ('LAK', 'LAK'), ('ERN', 'ERN'), ('SLL', 'SLL'), ('PLN', 'PLN'), ('JOD', 'JOD'), ('ILS', 'ILS'), ('AED', 'AED'), ('NPR', 'NPR'), ('NZD', 'NZD'), ('SGD', 'SGD'), ('JPY', 'JPY'), ('PAB', 'PAB'), ('ZMW', 'ZMW'), ('CZK', 'CZK'), ('SOS', 'SOS'), ('LTL', 'LTL'), ('KGS', 'KGS'), ('SHP', 'SHP'), ('BGN', 'BGN'), ('TOP', 'TOP'), ('MVR', 'MVR'), ('VEF02', 'VEF02'), ('TMT', 'TMT'), ('GMD', 'GMD'), ('MZN', 'MZN'), ('RSD', 'RSD'), ('MWK', 'MWK'), ('PGK', 'PGK'), ('MXN', 'MXN'), ('XAF', 'XAF'), ('VND', 'VND'), ('INR', 'INR'), ('NOK', 'NOK'), ('XPF', 'XPF'), ('SSP', 'SSP'), ('IQD', 'IQD'), ('SRD', 'SRD'), ('SAR', 'SAR'), ('XCD', 'XCD'), ('IRR', 'IRR'), ('KPW01', 'KPW01'), ('HTG', 'HTG'), ('IDR', 'IDR'), ('XOF', 'XOF'), ('ISK', 'ISK'), ('ANG', 'ANG'), ('NAD', 'NAD'), ('MMK', 'MMK'), ('STD', 'STD'), ('VUV', 'VUV'), ('LSL', 'LSL'), ('SVC', 'SVC'), ('KHR', 'KHR'), ('SZL', 'SZL'), ('RUB', 'RUB'), ('UAH', 'UAH'), ('UGX', 'UGX'), ('THB', 'THB'), ('AOA', 'AOA'), ('YER', 'YER'), ('USD', 'USD'), ('UZS', 'UZS'), ('OMR', 'OMR'), ('SBD', 'SBD'), ('TZS', 'TZS'), ('SDG', 'SDG'), ('WST', 'WST'), ('QAR', 'QAR'), ('MOP', 'MOP'), ('MRO', 'MRO'), ('VEF', 'VEF'), ('TRY', 'TRY'), ('ZAR', 'ZAR'), ('HUF', 'HUF'), ('MUR', 'MUR'), ('PHP', 'PHP'), ('BYN', 'BYN'), ('KRW', 'KRW'), ('TND', 'TND'), ('MNT', 'MNT'), ('PEN', 'PEN')], max_length=4, null=True)),
                ('total_local', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterventionPlannedVisits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('year', models.IntegerField(default=EquiTrack.utils.get_current_year)),
                ('programmatic_q1', models.IntegerField(default=0)),
                ('programmatic_q2', models.IntegerField(default=0)),
                ('programmatic_q3', models.IntegerField(default=0)),
                ('programmatic_q4', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Intervention Planned Visits',
            },
        ),
        migrations.CreateModel(
            name='InterventionReportingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateField(verbose_name='Reporting Period Start Date')),
                ('end_date', models.DateField(verbose_name='Reporting Period End Date')),
                ('due_date', models.DateField(verbose_name='Report Due Date')),
            ],
            options={
                'ordering': ['-due_date'],
            },
        ),
        migrations.CreateModel(
            name='InterventionResultLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterventionSectorLocationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('intervention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sector_locations', to='partners.Intervention')),
                ('locations', models.ManyToManyField(blank=True, related_name='intervention_sector_locations', to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PartnerOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('partner_type', models.CharField(choices=[('Bilateral / Multilateral', 'Bilateral / Multilateral'), ('Civil Society Organization', 'Civil Society Organization'), ('Government', 'Government'), ('UN Agency', 'UN Agency')], max_length=50, verbose_name='Partner Type')),
                ('cso_type', models.CharField(blank=True, choices=[('International', 'International'), ('National', 'National'), ('Community Based Organization', 'Community Based Organization'), ('Academic Institution', 'Academic Institution')], max_length=50, null=True, verbose_name='CSO Type')),
                ('name', models.CharField(help_text='Please make sure this matches the name you enter in VISION', max_length=255, verbose_name='Name')),
                ('short_name', models.CharField(blank=True, max_length=50, verbose_name='Short Name')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='Description')),
                ('shared_with', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('DPKO', 'DPKO'), ('ECA', 'ECA'), ('ECLAC', 'ECLAC'), ('ESCWA', 'ESCWA'), ('FAO', 'FAO'), ('ILO', 'ILO'), ('IOM', 'IOM'), ('OHCHR', 'OHCHR'), ('UN', 'UN'), ('UN Women', 'UN Women'), ('UNAIDS', 'UNAIDS'), ('UNDP', 'UNDP'), ('UNESCO', 'UNESCO'), ('UNFPA', 'UNFPA'), ('UN - Habitat', 'UN - Habitat'), ('UNHCR', 'UNHCR'), ('UNODC', 'UNODC'), ('UNOPS', 'UNOPS'), ('UNRWA', 'UNRWA'), ('UNSC', 'UNSC'), ('UNU', 'UNU'), ('WB', 'WB'), ('WFP', 'WFP'), ('WHO', 'WHO')], max_length=20), blank=True, null=True, size=None, verbose_name='Shared Partner')),
                ('street_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=64, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='Postal Code')),
                ('country', models.CharField(blank=True, max_length=64, null=True, verbose_name='Country')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(blank=True, max_length=64, null=True, verbose_name='Phone Number')),
                ('vendor_number', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Vendor Number')),
                ('alternate_id', models.IntegerField(blank=True, null=True, verbose_name='Alternate ID')),
                ('alternate_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alternate Name')),
                ('rating', models.CharField(blank=True, choices=[('High', 'High'), ('Significant', 'Significant'), ('Moderate', 'Medium'), ('Low', 'Low'), ('Non-Assessed', 'Non Required')], max_length=50, null=True, verbose_name='Risk Rating')),
                ('type_of_assessment', models.CharField(max_length=50, null=True, verbose_name='Assessment Type')),
                ('last_assessment_date', models.DateField(blank=True, null=True, verbose_name='Last Assessment Date')),
                ('core_values_assessment_date', models.DateField(blank=True, null=True, verbose_name='Date positively assessed against core values')),
                ('core_values_assessment', models.FileField(blank=True, help_text='Only required for CSO partners', max_length=1024, null=True, upload_to='partners/core_values/', verbose_name='Core Values Assessment')),
                ('vision_synced', models.BooleanField(default=False, verbose_name='VISION Synced')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('deleted_flag', models.BooleanField(default=False, verbose_name='Marked for deletion')),
                ('total_ct_cp', models.DecimalField(blank=True, decimal_places=2, help_text='Total Cash Transferred for Country Programme', max_digits=12, null=True, verbose_name='Total Cash Transferred for Country Programme')),
                ('total_ct_cy', models.DecimalField(blank=True, decimal_places=2, help_text='Total Cash Transferred per Current Year', max_digits=12, null=True, verbose_name='Total Cash Transferred per Current Year')),
                ('net_ct_cy', models.DecimalField(blank=True, decimal_places=2, help_text='Net Cash Transferred per Current Year', max_digits=12, null=True)),
                ('reported_cy', models.DecimalField(blank=True, decimal_places=2, help_text='Liquidations 1 Oct - 30 Sep', max_digits=12, null=True)),
                ('total_ct_ytd', models.DecimalField(blank=True, decimal_places=2, help_text='Cash Transfers Jan - Dec', max_digits=12, null=True)),
                ('hact_values', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=partners.models.hact_default, null=True, verbose_name='HACT')),
                ('basis_for_risk_rating', models.CharField(blank=True, max_length=50, null=True, verbose_name='Basis for Risk Rating')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(EquiTrack.mixins.AdminURLMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PartnerStaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Title')),
                ('first_name', models.CharField(max_length=64, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last Name')),
                ('email', models.CharField(max_length=128, unique=True, verbose_name='Email Address')),
                ('phone', models.CharField(blank=True, max_length=64, null=True, verbose_name='Phone Number')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_members', to='partners.PartnerOrganization', verbose_name='Partner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlannedEngagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('spot_check_mr', EquiTrack.fields.QuarterField(blank=True, choices=[(b'q1', b'Q1'), (b'q2', b'Q2'), (b'q3', b'Q3'), (b'q4', b'Q4')], max_length=2, null=True)),
                ('spot_check_follow_up_q1', models.IntegerField(default=0, verbose_name='Spot Check Q1')),
                ('spot_check_follow_up_q2', models.IntegerField(default=0, verbose_name='Spot Check Q2')),
                ('spot_check_follow_up_q3', models.IntegerField(default=0, verbose_name='Spot Check Q3')),
                ('spot_check_follow_up_q4', models.IntegerField(default=0, verbose_name='Spot Check Q4')),
                ('scheduled_audit', models.BooleanField(default=False, verbose_name='Scheduled Audit')),
                ('special_audit', models.BooleanField(default=False, verbose_name='Special Audit')),
                ('partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='planned_engagement', to='partners.PartnerOrganization', verbose_name='Partner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkspaceFileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='partnerorganization',
            unique_together=set([('name', 'vendor_number')]),
        ),
    ]
