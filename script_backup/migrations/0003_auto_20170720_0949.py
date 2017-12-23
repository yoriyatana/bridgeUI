# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('script_backup', '0002_auto_20170719_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='A1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.CreateModel(
            name='A2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.CreateModel(
            name='Ar1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.CreateModel(
            name='Ar2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.CreateModel(
            name='At1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.CreateModel(
            name='At2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('Model', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'db_table': 'script_backup_script_backup',
                'managed': True,
                'verbose_name_plural': 'Gateway',
            },
        ),
        migrations.AlterField(
            model_name='historicalscript_backup',
            name='Model',
            field=models.CharField(default=b'?', max_length=255, choices=[(b'Static-Ring', b'Static-Ring'), (b'VirPOP-Static', b'VirPOP-Static'), (b'Special', b'Special'), (b'Transit-TN', b'Transit-TN'), (b'Transit-QT', b'Transit-QT')]),
        ),
        migrations.AlterField(
            model_name='script_backup',
            name='Model',
            field=models.CharField(default=b'?', max_length=255, choices=[(b'Static-Ring', b'Static-Ring'), (b'VirPOP-Static', b'VirPOP-Static'), (b'Special', b'Special'), (b'Transit-TN', b'Transit-TN'), (b'Transit-QT', b'Transit-QT')]),
        ),
    ]
