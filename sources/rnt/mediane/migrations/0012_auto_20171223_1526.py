# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediane', '0011_auto_20171223_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='algorithm',
            name='public',
            field=models.BooleanField(default=False, help_text='Can it be seen by everyone?'),
        ),
        migrations.AddField(
            model_name='distance',
            name='public',
            field=models.BooleanField(default=False, help_text='Can it be seen by everyone?'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='public',
            field=models.BooleanField(default=False, help_text='Can it be seen by everyone?'),
        ),
    ]
