# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-26 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='addedDate',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='index',
            new_name='id',
        ),
        migrations.AddField(
            model_name='song',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='song',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='song',
            name='queueCounter',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='song',
            name='skipCounter',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]