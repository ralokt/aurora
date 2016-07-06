# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0002_add_filter_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspicion',
            name='state',
            field=models.CharField(choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED'), (4, 'SUSPECTED_SELF_PLAGIARISM'), (5, 'NOT_SUSPECTED')], max_length=2, default=0),
        ),
        migrations.AlterUniqueTogether(
            name='reference',
            unique_together=set([('hash', 'suspect_doc')]),
        ),
    ]
