# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 08:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170607_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='categorys',
            new_name='categories',
        ),
    ]
