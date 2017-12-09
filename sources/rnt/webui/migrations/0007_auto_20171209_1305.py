# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webui', '0006_dataset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='complete',
            field=models.BooleanField(default=True, help_text='Are every elements present in each rankings of the dataset'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='step',
            field=models.IntegerField(blank=True, help_text='The number of steps used to generate the dataset, if pertinent', null=True),
        ),
    ]
