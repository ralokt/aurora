# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-25 21:47
from __future__ import unicode_literals

import AuroraUser.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuroraUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('statement', models.TextField(blank=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=AuroraUser.models.avatar_path)),
                ('matriculation_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('study_code', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('oid', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
