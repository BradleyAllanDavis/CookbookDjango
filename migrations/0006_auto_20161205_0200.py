# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 02:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0005_auto_20161204_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookbook.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='cookbook.Tag'),
        ),
    ]