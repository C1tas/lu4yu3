# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170607_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
