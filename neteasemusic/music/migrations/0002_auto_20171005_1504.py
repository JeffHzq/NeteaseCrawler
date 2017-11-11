# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='music',
            name='singer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Singer', verbose_name='\u6b4c\u624b'),
        ),
        migrations.AlterField(
            model_name='music',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Album', verbose_name='\u4e13\u8f91'),
        ),
    ]