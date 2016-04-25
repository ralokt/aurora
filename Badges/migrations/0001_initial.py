# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '__first__'),
        ('AuroraUser', '0003_aurorauser_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('progress', models.IntegerField()),
                ('course', models.ForeignKey(to='Course.Course')),
                ('user', models.ForeignKey(to='AuroraUser.AuroraUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
