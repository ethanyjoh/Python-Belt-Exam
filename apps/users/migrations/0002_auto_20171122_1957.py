# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 19:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='Quote',
            new_name='quote',
        ),
    ]
