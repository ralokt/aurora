# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-25 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('AuroraUser', '0001_initial'),
        ('Elaboration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('submission_time', models.DateTimeField(null=True)),
                ('chosen_by', models.CharField(blank=True, default='random', max_length=100, null=True)),
                ('extra_review_question_answer', models.TextField(default='')),
                ('appraisal', models.CharField(choices=[('N', 'Not even trying'), ('F', 'Fail'), ('S', 'Success'), ('A', 'Awesome')], max_length=1, null=True)),
                ('elaboration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Elaboration.Elaboration')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuroraUser.AuroraUser')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_offset_min', models.IntegerField(default=0)),
                ('candidate_offset_max', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('appraisal', models.CharField(choices=[('P', 'Helpful Review'), ('D', 'Good Review'), ('B', 'Bad Review'), ('N', 'Negative Review')], default='D', max_length=1)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Review.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AuroraUser.AuroraUser')),
            ],
        ),
    ]
