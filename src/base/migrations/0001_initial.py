# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-26 21:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('addedDate', models.DateTimeField(auto_now=True)),
                ('queueCounter', models.IntegerField()),
                ('skipCounter', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('active', models.BooleanField()),
                ('type', models.IntegerField(choices=[(1, 'Web'), (2, 'Skype')])),
                ('login', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.User'),
        ),
    ]