# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalScript_Backup',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Gateway',
            },
        ),
        migrations.CreateModel(
            name='Script_Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Gateway', models.CharField(max_length=255)),
                ('IP', models.CharField(max_length=255)),
                ('Via', models.CharField(max_length=255)),
                ('File', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['Gateway'],
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateway',
            },
        ),
    ]
