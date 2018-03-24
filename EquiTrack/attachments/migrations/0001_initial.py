# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-24 13:36
from __future__ import unicode_literals

import attachments.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(blank=True, max_length=1024, null=True, upload_to=attachments.models.generate_file_path, verbose_name='File Attachment')),
                ('hyperlink', models.CharField(blank=True, max_length=255, null=True, verbose_name='Hyperlink')),
                ('object_id', models.IntegerField()),
                ('code', models.CharField(blank=True, max_length=64, verbose_name='Code')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='AttachmentFlat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(blank=True, max_length=255)),
                ('partner_type', models.CharField(blank=True, max_length=150)),
                ('vendor_number', models.CharField(blank=True, max_length=50)),
                ('pd_ssfa_number', models.CharField(blank=True, max_length=64)),
                ('file_type', models.CharField(blank=True, max_length=100)),
                ('file_link', models.CharField(blank=True, max_length=1024)),
                ('uploaded_by', models.CharField(blank=True, max_length=255)),
                ('created', models.CharField(max_length=50)),
                ('attachment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attachments.Attachment')),
            ],
        ),
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('label', models.CharField(max_length=64, verbose_name='Label')),
                ('code', models.CharField(default='', max_length=64, verbose_name='Code')),
            ],
            options={
                'ordering': ('code', 'order'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='filetype',
            unique_together=set([('name', 'code')]),
        ),
        migrations.AddField(
            model_name='attachment',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attachments.FileType', verbose_name='Document Type'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL, verbose_name='Uploaded By'),
        ),
    ]
