# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_tclist'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_toc',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
