# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('script_backup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalscript_backup',
            name='Model',
            field=models.CharField(default=b'?', max_length=255, choices=[(b'Static-Ring', b'Static-Ring'), (b'VirPOP-Static', b'VirPOP-Static'), (b'Special', b'Special'), (b'Transit', b'Transit')]),
        ),
        migrations.AddField(
            model_name='script_backup',
            name='Model',
            field=models.CharField(default=b'?', max_length=255, choices=[(b'Static-Ring', b'Static-Ring'), (b'VirPOP-Static', b'VirPOP-Static'), (b'Special', b'Special'), (b'Transit', b'Transit')]),
        ),
    ]
