# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediane', '0003_auto_20171219_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='transient',
            field=models.BooleanField(default=False, help_text='Should the dataset be deleted when the associated job is removed?'),
        ),
    ]
