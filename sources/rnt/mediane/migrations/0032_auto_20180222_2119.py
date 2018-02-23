# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediane', '0031_auto_20180221_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='m',
            field=models.IntegerField(default=0, help_text='The number of rankings'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='n',
            field=models.IntegerField(default=0, help_text='The number of elements'),
        ),
    ]
