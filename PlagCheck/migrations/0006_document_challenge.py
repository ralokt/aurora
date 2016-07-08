# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0005_reference_filter'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='challenge',
            field=models.CharField(default='', max_length=100),
            preserve_default=True,
        ),
    ]
