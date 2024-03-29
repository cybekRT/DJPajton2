# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-27 16:20
from __future__ import unicode_literals

from django.db import migrations, models
import time


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20191027_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='displayName',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.TextField(default=time.time),
        ),
    ]
