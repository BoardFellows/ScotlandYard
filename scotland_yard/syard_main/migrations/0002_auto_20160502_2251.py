# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 22:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('syard_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='round',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='syard_main.Game'),
        ),
    ]