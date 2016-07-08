# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PlagCheck', '0004_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterReference',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('hash', models.CharField(db_index=True, max_length=255)),
                ('suspect_doc', models.ForeignKey(to='PlagCheck.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='suspicion',
            name='state',
            field=models.CharField(default=0, choices=[(0, 'SUSPECTED'), (1, 'PLAGIARISM'), (2, 'FALSE_POSITIVE'), (3, 'CITED'), (4, 'SUSPECTED_SELF_PLAGIARISM'), (5, 'NOT_SUSPECTED')], max_length=2),
            preserve_default=True,
        ),
    ]
