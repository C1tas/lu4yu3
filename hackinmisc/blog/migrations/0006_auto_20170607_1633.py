# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170607_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]
