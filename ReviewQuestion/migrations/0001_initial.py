# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order', models.SmallIntegerField()),
                ('text', models.TextField(null=True)),
                ('boolean_answer', models.BooleanField(default=False)),
                ('visible_to_author', models.BooleanField(default=True)),
                ('challenge', models.ForeignKey(to='Challenge.Challenge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
