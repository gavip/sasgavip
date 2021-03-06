# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-13 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pipeline', '0005_auto_20161215_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(editable=False, max_length=50, null=True)),
                ('expected_runtime', models.IntegerField(default=0)),
                ('resources_ram_mb', models.IntegerField(default=2000, help_text=b'Amount of RAM (M) to be allocated for the AviJob')),
                ('resources_cpu_cores', models.IntegerField(default=1, help_text=b'Number of CPU cores to be allocated to the AviJob')),
                ('query', models.CharField(default=b"SELECT source_id, ra, dec, phot_g_mean_flux, phot_g_mean_mag, \n    DISTANCE(POINT('ICRS',ra,dec), POINT('ICRS',266.41683,-29.00781)) \n    AS dist FROM gaiadr1.gaia_source WHERE \n    1=CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))", max_length=1000)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='simplejob_model', to='pipeline.AviJobRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
