# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20170627_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(default='post', max_length=100),
        ),
    ]
