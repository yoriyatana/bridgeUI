# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_backup', '0003_auto_20170720_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='a1',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'A1'},
        ),
        migrations.AlterModelOptions(
            name='a2',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'A2'},
        ),
        migrations.AlterModelOptions(
            name='ar1',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'Ar1'},
        ),
        migrations.AlterModelOptions(
            name='ar2',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'Ar2'},
        ),
        migrations.AlterModelOptions(
            name='at1',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'At1'},
        ),
        migrations.AlterModelOptions(
            name='at2',
            options={'ordering': ['Gateway', 'Via'], 'managed': True, 'verbose_name': 'Gateway', 'verbose_name_plural': 'At2'},
        ),
        migrations.AlterModelOptions(
            name='script_backup',
            options={'ordering': ['Gateway', 'Via'], 'verbose_name': 'Gateway', 'verbose_name_plural': ' Gateway'},
        ),
    ]
