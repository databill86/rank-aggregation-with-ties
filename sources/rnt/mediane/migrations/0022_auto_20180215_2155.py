# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-15 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mediane', '0021_distance_id_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsToProduceDecorator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='result',
            old_name='results',
            new_name='consensuses',
        ),
        migrations.AddField(
            model_name='resultstoproducedecorator',
            name='result',
            field=models.ForeignKey(help_text='The result to produce', on_delete=django.db.models.deletion.CASCADE, to='mediane.Result'),
        ),
    ]
