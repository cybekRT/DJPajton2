# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-27 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20191027_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.User')),
            ],
        ),
    ]
