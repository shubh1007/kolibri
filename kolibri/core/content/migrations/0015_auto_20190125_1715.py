# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-26 01:15
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_auto_20181218_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channelmetadata',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='channelmetadata',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
